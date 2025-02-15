export function createPixelatedImage(src, pixelSize = 10) {
  return new Promise((resolve) => {
    const img = new Image();
    img.crossOrigin = 'Anonymous';
    img.onload = function () {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');

      const w = canvas.width = Math.floor(this.width / pixelSize);
      const h = canvas.height = Math.floor(this.height / pixelSize);

      ctx.drawImage(this, 0, 0, w, h);
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(canvas, 0, 0, w, h, 0, 0, this.width, this.height);

      resolve(canvas.toDataURL());
    };
    img.src = src;
  });
}