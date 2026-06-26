# codigo para criar as pastas do projectos

    mkdir site_web\backend\src\api,site_web\backend\src\core,site_web\backend\src\database,site_web\backend\src\services,site_web\backend\src\schemas,site_web\backend\src\utils,site_web\backend\tests,site_web\backend\migrations,site_web\frontend\templates,site_web\frontend\static\css,site_web\frontend\static\js,site_web\frontend\static\img




    /* ===== CARD COM GLASS EFFECT PROFISSIONAL ===== */
.event-card {
  position: relative;
  width: 320px;
  height: 420px;
  border-radius: 24px;
  overflow: hidden;
  flex-shrink: 0;
  scroll-snap-align: start;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Glass Effect */
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.event-card:hover {
  transform: translateY(-10px) scale(1.02);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.5);
}

.event-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
  transition: transform 0.5s;
  filter: brightness(0.9);
}

.event-card:hover img {
  transform: scale(1.08);
  filter: brightness(1);
}

/* Glass na parte de baixo do conteúdo */
.card-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 24px;
  z-index: 3;
  color: #fff;
  
  /* Glass Effect na área do texto */
  background: rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(16px) saturate(150%);
  -webkit-backdrop-filter: blur(16px) saturate(150%);
  border-top: 1px solid rgba(255, 255, 255, 0.15);
}

/* Badge DESTAQUE com glass */
.card-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  background: rgba(251, 191, 36, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: #000;
  padding: 8px 16px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
  z-index: 3;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 20px rgba(251, 191, 36, 0.4);
}

/* Data com glass */
.card-date {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 16px;
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 3;
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-date .day {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1;
}

.card-date .month {
  font-size: 12px;
  font-weight: 600;
  color: #4b5563;
  text-transform: uppercase;
  margin-top: 2px;
}

/* Tag com glass */
.card-meta .tag {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  padding: 4px 12px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.3px;
  transition: all 0.3s;
}

.card-meta .tag:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
}

/* Gradiente mais suave pra combinar com glass */
.card-gradient {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 70%;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 100%);
  z-index: 1;
}

/* Fundo do carrossel também com glass sutil */
.events-carousel {
  padding: 60px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
  position: relative;
}

.events-carousel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(40px);
  z-index: 0;
}

.carousel-header, .carousel-wrapper {
  position: relative;
  z-index: 1;
}

.carousel-header h2 {
  color: #fff;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.nav-btn {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
}

.nav-btn:hover {
  background: rgba(37, 99, 235, 0.9);
  border-color: rgba(255, 255, 255, 0.5);
}

/* Dots com glass */
.dot {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(4px);
}

.dot.active {
  background: #fff;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.6);
}















<div class="post-grid">
  
  <!-- CARD 1: POSTE GALVANIZADO 9M -->
  <div class="post-card">
    <!-- Lado Esquerdo: Imagem -->
    <div class="post-image-wrap">
      <div class="post-image-main">
        <img id="mainImage1" src="../static/assets/img/images.jpg" alt="Poste Galvanizado 9m">
      </div>
      
      <div class="post-thumbs">
        <img src="../static/assets/img/1.jpg" onclick="trocarImagem(this, 'mainImage1')" class="active" alt="Vista 1">
        <img src="../static/assets/img/2.jpg" onclick="trocarImagem(this, 'mainImage1')" alt="Vista 2">
        <img src="../static/assets/img/images.jpg" onclick="trocarImagem(this, 'mainImage1')" alt="Vista 3">
        <img src="../static/assets/img/images.jpg" onclick="trocarImagem(this, 'mainImage1')" alt="Vista 4">
      </div>
    </div>

    <!-- Lado Direito: Conteúdo -->
    <div class="post-content">
      <h2 class="post-title">Poste Galvanizado 9m</h2>
      <p class="post-code">COD: PST-009</p>
      <p class="post-price">AOA <span>45.000</span></p>
      
      <p class="post-section">Benefícios</p>
      <ul class="post-list">
        <li>Alta resistência à corrosão</li>
        <li>Instalação rápida e segura</li>
        <li>Durabilidade +15 anos</li>
        <li>Ideal para iluminação pública</li>
      </ul>

      <button class="btn-post">PEDIR ORÇAMENTO</button>
    </div>
  </div>

  <!-- CARD 2: POSTE DECORATIVO 6M -->
  <div class="post-card">
    <!-- Lado Esquerdo: Imagem -->
    <div class="post-image-wrap">
      <div class="post-image-main">
        <img id="mainImage2" src="../static/assets/img/images.jpg" alt="Poste Decorativo 6m">
      </div>
      
      <div class="post-thumbs">
        <img src="../static/assets/img/images.jpg" onclick="trocarImagem(this, 'mainImage2')" class="active" alt="Vista 1">
        <img src="../static/assets/img/images.jpg" onclick="trocarImagem(this, 'mainImage2')" alt="Vista 2">
        <img src="../static/assets/img/images.jpg" onclick="trocarImagem(this, 'mainImage2')" alt="Vista 3">
        <img src="../static/assets/img/images.jpg" onclick="trocarImagem(this, 'mainImage2')" alt="Vista 4">
      </div>
    </div>

    <!-- Lado Direito: Conteúdo -->
    <div class="post-content">
      <h2 class="post-title">Poste Decorativo 6m</h2>
      <p class="post-code">COD: PST-006</p>
      <p class="post-price">AOA <span>32.000</span></p>
      

      <p class="post-section">Benefícios</p>
      <ul class="post-list">
        <li>Design moderno para jardins</li>
        <li>Base reforçada anti-vibração</li>
        <li>Acabamento premium</li>
        <li>Resistente ao sol e chuva</li>
      </ul>

      <button class="btn-post">PEDIR ORÇAMENTO</button>
    </div>
  </div>

</div>


