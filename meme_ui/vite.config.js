import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'

// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    vue({
      template: { transformAssetUrls }
    }),

    quasar({
      autoImportComponentCase: 'pascal',
      sassVariables: 'src/quasar-variables.sass'
    })
  ],
  server: {
    proxy: {
      "^/(meme|tag|user|raw|thumbnail)": {
        target: "http://localhost:8000/meme",
        changeOrigin: true
      }
    }
  }
})
