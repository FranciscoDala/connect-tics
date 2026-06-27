// ============================================================================
// Buscar os postes novos e destacados do banco de dados =====
// ============================================================================
document.addEventListener("DOMContentLoaded", async () => {
    const track = document.getElementById("carouselTrack");
    
    if (!track) return; // Só roda na home

    try {
        const res = await fetch("/admin/posts?limit=20"); // <-- Aumentei pra 20 pra ter mais chance de filtrar
        if (!res.ok) throw new Error(`Erro ${res.status} ao buscar posts`);
        const allPosts = await res.json();

        const now = new Date();
        const THREE_DAYS_MS = 3 * 24 * 60 * 60 * 1000;

        // ===================================================================
        // FILTRO: SÓ NOVOS OU DESTACADOS
        // ===================================================================
        const filteredPosts = allPosts.filter(post => {
            const isHighlighted = post.is_highlighted === true;
            const isNew = (now - new Date(post.created_at)) < THREE_DAYS_MS;
            return isHighlighted || isNew; // <-- Regra: Destaque OU Novo
        }).slice(0, 8); // <-- Pega só os 8 primeiros depois do filtro
        // ===================================================================

        if (filteredPosts.length === 0) {
            track.innerHTML = `<p style="padding: 40px;">Nenhum post novo ou em destaque.</p>`;
            return;
        }

        track.innerHTML = ""; 

        filteredPosts.forEach((post) => {
            const imgUrl = post.cover_image || "/static/assets/img/placeholder.jpg";
            const date = new Date(post.created_at);
            const day = date.getDate();
            const month = date.toLocaleString("pt-PT", { month: "short" }).toUpperCase();

            let badge = "";
            if (post.is_highlighted) {
                badge = `<span class="card-badge">Destaque</span>`;
            } else { // Se não é destaque, e passou no filtro, é porque é Novo
                badge = `<span class="card-badge novo">Novo</span>`;
            }

            const card = `
                <a href="/galeria/${post.id}" class="event-card-link">
                    <div class="event-card">
                        <div class="card-image-wrapper">
                            <img src="${imgUrl}" alt="${post.title}">
                        </div>
                        <div class="card-gradient"></div>
                        ${badge} 
                        <div class="card-date">
                            <span class="day">${day}</span>
                            <span class="month">${month}</span>
                        </div>
                        <div class="card-content">
                            <h3>${post.title}</h3>
                            <div class="card-meta">
                                <span class="tag">${post.category_name || post.type}</span>
                                <span>${date.toLocaleTimeString("pt-PT", {hour: '2-digit', minute:'2-digit'})}H</span>
                            </div>
                        </div>
                    </div>
                </a>
            `;
            track.insertAdjacentHTML("beforeend", card);
        });

        if (typeof initCarousel === "function") {
            initCarousel();
        }

    } catch (error) {
        console.error(error);
        track.innerHTML = `<p style="padding: 40px; color:red;">Erro ao carregar posts.</p>`;
    }
});










// ============================================================================
// Buscar as fotos todas no banco de dados =====
// ============================================================================
document.addEventListener("DOMContentLoaded", async () => {
    const principal = document.getElementById('foto-principal');
    const miniaturasWrap = document.getElementById('miniaturas');
    const nomeFotoEl = document.getElementById('nome-foto');
    const contador = document.getElementById('contador-fotos');
    const countLike = document.getElementById('count-like');
    const countDislike = document.getElementById('count-dislike');
    const parecidasWrap = document.getElementById('fotos-parecidas'); // <-- PEGOU A DIV DA DIREITA

    if (!principal ||!miniaturasWrap) return; 

    let fotoAtual = 0;
    let userVote = 0; 
    let album = []; 

    // 1. BUSCA TODOS OS POSTS TIPO 'FOTOS'
    try {
        const res = await fetch("/admin/posts?limit=100");
        if (!res.ok) throw new Error(`Erro ${res.status}`);
        const posts = await res.json();

        const postsFotos = posts.filter(p => p.type === 'fotos');

        postsFotos.forEach(post => {
            post.images.forEach(img => {
                album.push({
                    image_url: img.image_url,
                    image_id: img.id,
                    post_title: post.title,
                    likes: img.likes,
                    dislikes: img.dislikes,
                    created_at: post.created_at,
                    post_id: post.id // <-- GUARDEI O ID DO POST
                });
            });
        });

    } catch (error) {
        console.error("Erro ao carregar álbum:", error);
        return;
    }

    if (album.length === 0) {
        principal.src = "/static/assets/img/placeholder.jpg";
        nomeFotoEl.textContent = "Nenhuma foto publicada";
        return;
    }

    // 2. FUNÇÃO PARA ATUALIZAR TUDO
    function att() {
        const foto = album[fotoAtual];
        principal.src = foto.image_url;
        nomeFotoEl.textContent = foto.post_title;
        contador.textContent = `Foto ${fotoAtual + 1} de ${album.length}`;
        countLike.textContent = foto.likes;
        countDislike.textContent = foto.dislikes;
        userVote = 0; 

        document.querySelectorAll('#miniaturas img').forEach((img, i) => {
            img.classList.toggle('ativa', i === fotoAtual);
        });

        carregarParecidas(foto.post_id); // <-- CHAMA AS PARECIDAS AO TROCAR
    }

    // 3. NOVA FUNÇÃO: CARREGA "FOTOS PARECIDAS" DA DIREITA
    function carregarParecidas(postIdAtual) {
        // Pega 4 fotos do mesmo post, excluindo a foto atual
        const parecidas = album
           .filter(f => f.post_id === postIdAtual && f.image_url!== album[fotoAtual].image_url)
           .slice(0, 4);

        if (parecidas.length === 0) {
            parecidasWrap.innerHTML = `<p style="font-size:14px; color:#aaa;">Sem outras fotos neste post.</p>`;
            return;
        }

        parecidasWrap.innerHTML = parecidas.map(f => `
            <div class="parecida-item" onclick="setFoto(${album.findIndex(x => x.image_id === f.image_id)})" style="cursor:pointer;">
                <img src="${f.image_url}">
                <div><strong>${f.post_title}</strong><small>${f.likes} Likes</small></div>
            </div>
        `).join('');
    }

    // 4. MONTA AS MINIATURAS EM BAIXO
    miniaturasWrap.innerHTML = album.map((foto, i) =>
        `<img src="${foto.image_url}" class="mini" onclick="setFoto(${i})" alt="${foto.post_title}">`
    ).join('');

    // 5. FUNÇÕES GLOBAIS
    window.setFoto = (i) => { fotoAtual = i; att(); }
    window.mudarSlide = (d) => { 
        fotoAtual = (fotoAtual + d + album.length) % album.length; 
        att(); 
    }

    window.darLike = async () => {
        const foto = album[fotoAtual];
        if (userVote === 1) return;
        if (userVote === -1) foto.dislikes--;
        foto.likes++;
        userVote = 1;
        att();
        await fetch(`/admin/posts/images/${foto.image_id}/like`, { method: 'POST' });
    }

    window.darDislike = async () => {
        const foto = album[fotoAtual];
        if (userVote === -1) return;
        if (userVote === 1) foto.likes--;
        foto.dislikes++;
        userVote = -1;
        att();
        await fetch(`/admin/posts/images/${foto.image_id}/dislike`, { method: 'POST' });
    }

    // 6. INICIA
    att();
});