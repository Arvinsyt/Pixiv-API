<template>
  <!-- 扇形展开的“作品卡”插画,呼应 Pixiv 的画廊属性 -->
  <svg class="hero-art" viewBox="0 0 300 320" fill="none" aria-hidden="true">
    <!-- 左后卡片:夜空 -->
    <g class="card card-back">
      <rect x="18" y="52" width="150" height="196" rx="20" fill="var(--art-card)" stroke="var(--art-line)" stroke-width="1.5" />
      <rect x="30" y="64" width="126" height="126" rx="12" fill="var(--art-sky-deep)" />
      <circle cx="128" cy="88" r="14" fill="var(--art-card)" opacity="0.9" />
      <path d="M30 158 Q 62 128 93 158 T 156 158" stroke="var(--art-card)" stroke-width="3" opacity="0.7" />
      <path d="M30 174 Q 62 148 93 174 T 156 174" stroke="var(--art-card)" stroke-width="3" opacity="0.45" />
      <rect x="30" y="202" width="86" height="8" rx="4" fill="var(--art-bar)" />
      <rect x="30" y="218" width="54" height="8" rx="4" fill="var(--art-bar)" opacity="0.6" />
    </g>

    <!-- 右后卡片:蓝色画布 + 星光 -->
    <g class="card card-back">
      <rect x="128" y="64" width="150" height="196" rx="20" fill="var(--art-card)" stroke="var(--art-line)" stroke-width="1.5" />
      <rect x="140" y="76" width="126" height="126" rx="12" fill="var(--art-sky-soft)" />
      <path class="spark spark-big" d="M203 118 C204.5 129 208 132.5 219 134 C208 135.5 204.5 139 203 150 C201.5 139 198 135.5 187 134 C198 132.5 201.5 129 203 118 Z" fill="var(--art-blue)" />
      <circle cx="168" cy="168" r="7" fill="var(--art-blue)" opacity="0.5" />
      <circle cx="238" cy="176" r="5" fill="var(--art-blue)" opacity="0.35" />
      <rect x="140" y="214" width="94" height="8" rx="4" fill="var(--art-bar)" />
      <rect x="140" y="230" width="60" height="8" rx="4" fill="var(--art-bar)" opacity="0.6" />
    </g>

    <!-- 前卡片:晴空 + 心形收藏 -->
    <g class="card card-front">
      <rect x="62" y="28" width="176" height="232" rx="22" fill="var(--art-card)" stroke="var(--art-line)" stroke-width="2" />
      <rect x="76" y="42" width="148" height="148" rx="14" fill="url(#hero-sky)" />
      <path
        d="M150 148 C150 148 118 128 118 106 C118 93 128 84 140 84 C145 84 149 86 150 89 C151 86 155 84 160 84 C172 84 182 93 182 106 C182 128 150 148 150 148 Z"
        fill="var(--art-blue)"
      />
      <circle cx="102" cy="72" r="10" fill="var(--art-card)" opacity="0.85" />
      <rect x="76" y="204" width="104" height="10" rx="5" fill="var(--art-bar)" />
      <rect x="76" y="222" width="66" height="10" rx="5" fill="var(--art-bar)" opacity="0.6" />
      <rect x="184" y="202" width="26" height="26" rx="9" fill="var(--art-blue-soft)" />
      <path d="M197 220.5 C197 220.5 188.5 215.5 188.5 209.8 C188.5 207 190.7 205 193.2 205 C194.9 205 196.3 205.8 197 206.9 C197.7 205.8 199.1 205 200.8 205 C203.3 205 205.5 207 205.5 209.8 C205.5 215.5 197 220.5 197 220.5 Z" fill="var(--art-blue)" />
    </g>

    <!-- 散落的星光 -->
    <path class="spark spark-small s1" d="M42 34 C42.9 40.5 45 42.6 51.5 43.5 C45 44.4 42.9 46.5 42 53 C41.1 46.5 39 44.4 32.5 43.5 C39 42.6 41.1 40.5 42 34 Z" fill="var(--art-blue)" opacity="0.7" />
    <path class="spark spark-small s2" d="M268 300 C268.9 306.5 271 308.6 277.5 309.5 C271 310.4 268.9 312.5 268 319 C267.1 312.5 265 310.4 258.5 309.5 C265 308.6 267.1 306.5 268 300 Z" fill="var(--art-blue)" opacity="0.45" />

    <defs>
      <linearGradient id="hero-sky" x1="76" y1="42" x2="224" y2="190" gradientUnits="userSpaceOnUse">
        <stop style="stop-color: var(--art-sky-top)" />
        <stop offset="1" style="stop-color: var(--art-sky-btm)" />
      </linearGradient>
    </defs>
  </svg>
</template>

<style scoped>
.hero-art {
  width: min(300px, 72vw);
  height: auto;
  animation: art-float 6s ease-in-out infinite;
}

.card {
  transform-box: fill-box;
  transform-origin: center;
}

.card-back:first-of-type {
  transform: rotate(-9deg) translate(-6px, 12px);
}

.card-back:nth-of-type(2) {
  transform: rotate(8deg) translate(6px, 8px);
}

.spark-big {
  animation: spark-twinkle 3.2s ease-in-out infinite;
}

.spark-small.s2 {
  animation: spark-twinkle 3.2s ease-in-out 1.1s infinite;
}

@media (prefers-reduced-motion: reduce) {
  .hero-art,
  .spark-big,
  .spark-small {
    animation: none;
  }
}

@keyframes art-float {
  50% {
    transform: translateY(-9px);
  }
}

@keyframes spark-twinkle {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.35;
  }
}
</style>
