<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import HeroArt from './components/HeroArt.vue'
</script>

<template>
  <DefaultTheme.Layout>
    <template #home-hero-image><HeroArt /></template>
  </DefaultTheme.Layout>
</template>
