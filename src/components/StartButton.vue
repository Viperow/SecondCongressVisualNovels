<template>
  <button class="start-btn" @click="$emit('click')">开 始 游 戏</button>
</template>

<style scoped>
.start-btn {
  z-index: 100;
  font-size: 3rem;
  padding: 1rem 2rem;
  position: absolute;
  top: 80%;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.896);
  cursor: pointer;
  overflow: hidden;
  /* animation: pulse 2s infinite ease-in-out; */
  transition: transform 0.3s ease;
  font-weight: bold;
  
}

.start-btn:hover {
  transform: scale(1.1);
}

.start-btn::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%); /* 居中到按钮中线 */
  width: 0;
  height: 100%;
  background: url('/assets/effects/brush-stroke.png') no-repeat left center;
  background-size: cover;
  z-index: -1; /* 在按钮文本下面 */
  transition: width 0.2s ease-in-out;
}

.start-btn:hover::before {
  width: 100%; /* hover时刷开整条 */
}

@keyframes pulse {
  0% { transform: scale(1); box-shadow: 0 0 10px rgba(255,193,7,0.5); }
  50% { transform: scale(1.05); box-shadow: 0 0 20px rgba(255,193,7,0.8); }
  100% { transform: scale(1); box-shadow: 0 0 10px rgba(255,193,7,0.5); }
}
</style>