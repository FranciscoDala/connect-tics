const btnLogin = document.querySelector('.btn-login'); // Linha 7
const btnClose = document.querySelector('.modal-close'); // Linha 8
const form = document.getElementById('loginForm'); // Linha 10

// ============================================================================
// Botão de pesquisa e Modal =====
// ============================================================================
function toggleSearch() {
    const searchBlock = document.getElementById('searchBlock');
    searchBlock.classList.toggle('show'); // adiciona/remove a classe 'show'

    // Se abriu, já foca no input pra digitar
    if (searchBlock.classList.contains('show')) {
        document.querySelector('.search-input').focus();
    }
}

// Fecha clicando no X
document.getElementById('closeSearch').onclick = () => {
    document.getElementById('searchBlock').classList.remove('show');
}

// Fecha clicando fora da caixa azul
document.getElementById('searchBlock').onclick = (e) => {
    if (e.target.id === 'searchBlock') {
        document.getElementById('searchBlock').classList.remove('show');
    }
}






// ============================================================================
// Login Modal =====
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {

    // ===== 1. PEGA OS ELEMENTOS =====
    const modal = document.getElementById('loginModal'); // Tua .modal-overlay
    const btnLogin = document.querySelector('.btn-login'); // Botão "Login" do menu
    const btnClose = document.querySelector('.modal-close'); // X
    const form = document.getElementById('loginForm');

    function showAlert(icon, title, text) {
        Swal.fire({
            width: '400px', icon: icon, title: title, text: text,
            confirmButtonColor: icon === 'error' ? '#d33' : '#3085d6',
            background: '#1a1a1a', color: '#fff'
        });
    }

    // ===== 2. ABRIR / FECHAR MODAL CUSTOM =====
    // Abre: só adiciona .active
    btnLogin?.addEventListener('click', (e) => {
        e.preventDefault(); // Se for <a href="#">
        modal?.classList.add('active');
    });

    // Fecha: no X
    btnClose?.addEventListener('click', () => modal?.classList.remove('active'));

    // Fecha: clicando fora
    modal?.addEventListener('click', (e) => { 
        if (e.target === modal) modal.classList.remove('active'); 
    });

    // ===== 3. LOGIN VIA AJAX - SEM RECARREGAR =====
    form?.addEventListener('submit', async (e) => {
        e.preventDefault(); // TRAVA O RECARREGAMENTO

        const username = document.getElementById('username')?.value.trim();
        const password = document.getElementById('password')?.value.trim();

        if (username === '' || password === '') {
            showAlert('warning', 'Atenção', 'Preencha usuário e senha');
            return;
        }

        const formData = new FormData(form);
        try {
            const response = await fetch('/login', { method: 'POST', body: formData });
            const data = await response.json();

            if (response.ok) { // 200
                modal.classList.remove('active'); // Fecha tua modal custom
                window.location.href = data.redirect; // Vai pro /admin
            } else { // 401
                showAlert('error', 'Oops...', data.detail); // Fica aberta + SweetAlert
            }
        } catch (error) {
            showAlert('error', 'Erro', 'Servidor fora do ar');
        }
    });
});












// ============================================================================
// Modal de pesquisa =====
// ============================================================================
const searchBlock = document.getElementById('searchBlock');
const searchIcon = document.querySelector('.search-icon'); // tua lupa do menu
const closeSearch = document.getElementById('closeSearch');

searchIcon.onclick = () => {
    searchBlock.classList.add('show');
    document.querySelector('.search-input').focus();
}

closeSearch.onclick = () => searchBlock.classList.remove('show');

// Fecha clicando fora da caixa azul
searchBlock.onclick = (e) => {
    if (e.target === searchBlock) searchBlock.classList.remove('show');
}










// ============================================================================
// Menu lateral =====
// ============================================================================
function abrirMenu() {
    document.getElementById('overlay').classList.add('active');
}

function fecharMenu(e) {
    if (e.target.id === 'overlay' || e.target.classList.contains('close-btn')) {
        document.getElementById('overlay').classList.remove('active');
    }
}

function toggle(btn) {
    let submenu = btn.nextElementSibling;
    let arrow = btn.querySelector('.arrow');

    if (submenu && submenu.classList.contains('submenu')) {
        submenu.classList.toggle('show');
        if (arrow) {
            arrow.innerHTML = submenu.classList.contains('show') ? '▲' : '▼';
        }
    }
}



// ============================================================================
// Menu Desktop com click para pc =====
// ============================================================================
document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.menu-desktop > .item > .item-btn');

    menuItems.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            let submenu = this.nextElementSibling;

            // Fecha todos os outros submenus
            document.querySelectorAll('.menu-desktop .submenu.open').forEach(openSub => {
                if (openSub !== submenu) {
                    openSub.classList.remove('open');
                    let openBtn = openSub.previousElementSibling;
                    if (openBtn && openBtn.querySelector('.arrow')) {
                        openBtn.querySelector('.arrow').innerHTML = '▼';
                    }
                }
            });

            // Abre/fecha o submenu clicado
            if (submenu && submenu.classList.contains('submenu')) {
                submenu.classList.toggle('open');
                let arrow = this.querySelector('.arrow');
                if (arrow) {
                    arrow.innerHTML = submenu.classList.contains('open') ? '▲' : '▼';
                }
            }
        });
    });

    // ============================================================================
    // Sub-submenus - Serviços para Cidadão, Empresa, etc =====
    // ============================================================================
    const subMenuItems = document.querySelectorAll('.menu-desktop .submenu > .item > .item-btn');
    subMenuItems.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            let submenu = this.nextElementSibling;

            // Fecha outros sub-submenus do mesmo nível
            let parentSubmenu = this.closest('.submenu');
            parentSubmenu.querySelectorAll('.submenu.open').forEach(openSub => {
                if (openSub !== submenu) {
                    openSub.classList.remove('open');
                    let openBtn = openSub.previousElementSibling;
                    if (openBtn && openBtn.querySelector('.arrow')) {
                        openBtn.querySelector('.arrow').innerHTML = '▶';
                    }
                }
            });

            // Abre/fecha o sub-submenu clicado
            if (submenu && submenu.classList.contains('submenu')) {
                submenu.classList.toggle('open');
                let arrow = this.querySelector('.arrow');
                if (arrow) {
                    arrow.innerHTML = submenu.classList.contains('open') ? '▼' : '▶';
                }
            }
        });
    });

    // Fecha menu ao clicar fora
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.menu-desktop')) {
            document.querySelectorAll('.menu-desktop .submenu.open').forEach(sub => {
                sub.classList.remove('open');
            });
            document.querySelectorAll('.menu-desktop .arrow').forEach(arrow => {
                if (arrow.innerHTML === '▲') arrow.innerHTML = '▼';
                if (arrow.innerHTML === '▶') arrow.innerHTML = '▶';
            });
        }
    });
});


// ============================================================================
// Card carouselTrack =====
// ============================================================================
const track = document.getElementById('carouselTrack');
const dotsContainer = document.getElementById('carouselDots');

let isDown = false;
let startX;
let scrollLeft;
let cardWidth = 0;
let gap = 0;

const cards = track.querySelectorAll('.event-card');
cards.forEach((_, i) => {
    const dot = document.createElement('div');
    dot.classList.add('dot');
    if (i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => scrollToCard(i));
    dotsContainer.appendChild(dot);
});
const dots = dotsContainer.querySelectorAll('.dot');

function updateCardWidth() {
    const card = track.querySelector('.event-card');
    // GAP SÓ NO MOBILE/TABLET < 1024px
    gap = window.innerWidth < 1024 ? 30 : 0;
    cardWidth = card.offsetWidth + gap;
}

function scrollToCard(index) {
    const viewportWidth = window.innerWidth;
    const card = track.querySelector('.event-card');
    const cardActualWidth = card.offsetWidth;
    const scrollPos = index * cardWidth - (viewportWidth - cardActualWidth) / 2;
    track.scrollTo({ left: scrollPos, behavior: 'smooth' });
    updateDots(index);
}

function updateDots(activeIndex) {
    dots.forEach((dot, i) => dot.classList.toggle('active', i === activeIndex));
}

function snapToCenter() {
    const viewportWidth = window.innerWidth;
    const card = track.querySelector('.event-card');
    const cardActualWidth = card.offsetWidth;
    const scrollPos = track.scrollLeft;
    const cardIndex = Math.round((scrollPos + (viewportWidth - cardActualWidth) / 2) / cardWidth);
    scrollToCard(cardIndex);
}

track.addEventListener('mousedown', (e) => {
    isDown = true;
    track.style.cursor = 'grabbing';
    track.style.scrollSnapType = 'none';
    startX = e.pageX - track.offsetLeft;
    scrollLeft = track.scrollLeft;
});

track.addEventListener('mouseleave', () => {
    if (isDown) {
        isDown = false;
        track.style.cursor = 'grab';
        track.style.scrollSnapType = 'x mandatory';
        snapToCenter();
    }
});

track.addEventListener('mouseup', () => {
    isDown = false;
    track.style.cursor = 'grab';
    track.style.scrollSnapType = 'x mandatory';
    snapToCenter();
});

track.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - track.offsetLeft;
    const walk = x - startX;
    track.scrollLeft = scrollLeft - walk;
});

let touchStartX = 0;
track.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].pageX;
    scrollLeft = track.scrollLeft;
    track.style.scrollSnapType = 'none';
}, { passive: true });

track.addEventListener('touchmove', (e) => {
    const touchX = e.touches[0].pageX;
    const diff = touchStartX - touchX;
    track.scrollLeft = scrollLeft + diff;
}, { passive: true });

track.addEventListener('touchend', () => {
    track.style.scrollSnapType = 'x mandatory';
    snapToCenter();
}, { passive: true });

window.addEventListener('load', () => {
    updateCardWidth();
    scrollToCard(0);
});

window.addEventListener('resize', () => {
    updateCardWidth();
    const viewportWidth = window.innerWidth;
    const card = track.querySelector('.event-card');
    const cardActualWidth = card.offsetWidth;
    const activeIndex = Math.round((track.scrollLeft + (viewportWidth - cardActualWidth) / 2) / cardWidth);
    scrollToCard(activeIndex);
});









// ============================================================================
// Card-Post tricar a imagens pequenas =====
// ============================================================================
function trocarImagem(thumb, mainId) {
    document.getElementById(mainId).src = thumb.src; // usa a src direta

    thumb.parentElement.querySelectorAll('img').forEach(img => {
        img.classList.remove('active');
    });
    thumb.classList.add('active');
}

