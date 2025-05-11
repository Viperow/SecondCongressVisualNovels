<template>
  <div class="particle-wrapper">
    <canvas v-for="type in types" :key="type" :ref="el => registerCanvas(type, el)" class="particle-canvas" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue'

const props = defineProps<{
  types: ('stars' | 'dots' | 'snow' | 'sunrays')[]
}>()

const canvases: Record<string, HTMLCanvasElement> = {}

function registerCanvas(type: string, el: HTMLCanvasElement | null) {
  if (el) canvases[type] = el
}
function drawDots(ctx: CanvasRenderingContext2D, width: number, height: number) {
  const particles = Array.from({ length: 100 }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    r: Math.random() * 2 + 1,
    dx: (Math.random() - 0.5) * 0.5,
    dy: (Math.random() - 0.5) * 0.5
  }))

  width = window.innerWidth
  height = window.innerHeight

  function draw() {
    ctx.clearRect(0, 0, width, height)
    for (const p of particles) {
      ctx.beginPath()
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      ctx.fillStyle = '#ffffff88'
      ctx.fill()
      p.x += p.dx
      p.y += p.dy

      if (p.x < 0 || p.x > width) p.dx *= -1
      if (p.y < 0 || p.y > height) p.dy *= -1
    }
    requestAnimationFrame(draw)
  }

  draw()
}

function drawStars(ctx: CanvasRenderingContext2D, width: number, height: number) {
  const stars = Array.from({ length: 100 }, () => ({
    x: Math.random() * width,
    y: Math.random() * height,
    r: Math.random() * 1.5 + 0.5,
    alpha: Math.random()
  }))

  function draw() {
    ctx.clearRect(0, 0, width, height)
    for (const star of stars) {
      ctx.beginPath()
      ctx.arc(star.x, star.y, star.r, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(255, 255, 255, ${star.alpha})`
      ctx.fill()
      star.alpha += (Math.random() - 0.5) * 0.02
      if (star.alpha < 0.1) star.alpha = 0.1
      if (star.alpha > 1) star.alpha = 1
    }
    requestAnimationFrame(draw)
  }
  draw()
}

function drawSunrays(ctx: CanvasRenderingContext2D, width: number, height: number) {
  const rays = Array.from({ length: 5 }, (_, i) => ({
    angle: 20 + i * 10,
    opacity: Math.random() * 0.3 + 0.1
  }))

  function draw() {
    ctx.clearRect(0, 0, width, height)
    for (let i = 0; i < rays.length; i++) {
      const ray = rays[i]
      const x = 0
      const y = height
      const angle = (ray.angle * Math.PI) / 180
      const length = width * 2
      ctx.beginPath()
      ctx.moveTo(x, y)
      ctx.lineTo(x + Math.cos(angle) * length, y - Math.sin(angle) * length)
      ctx.lineWidth = 60
      ctx.strokeStyle = `rgba(255, 255, 200, ${ray.opacity})`
      ctx.stroke()

      // animate flicker
      ray.opacity += (Math.random() - 0.5) * 0.01
      if (ray.opacity < 0.05) ray.opacity = 0.05
      if (ray.opacity > 0.4) ray.opacity = 0.4
    }
    requestAnimationFrame(draw)
  }

  draw()
}

onMounted(() => {
  for (const type of props.types) {
    const canvas = canvases[type]
    if (!canvas) continue
    const ctx = canvas.getContext('2d')!
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    switch (type) {
      case 'dots':
        drawDots(ctx, canvas.width, canvas.height)
        break
      case 'stars':
        drawStars(ctx, canvas.width, canvas.height)
        break
      case 'sunrays':
        drawSunrays(ctx, canvas.width, canvas.height)
        break
    }
  }
})

onBeforeUnmount(() => {
  // could later cleanup animation frame
})
</script>

<style scoped>
.particle-wrapper {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.particle-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
</style>