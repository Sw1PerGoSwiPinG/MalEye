<template>
  <div>
    <div class="app-content">
      <vue-pdf-embed ref="pdfRef" :source="pdfSource" :page="page"
        @password-requested="handlePasswordRequest"
        @rendered="handleDocumentRender" />
    </div>
  </div>
</template>

<script>
import VuePdfEmbed from 'vue-pdf-embed'

export default {
  components: {
    VuePdfEmbed
  },
  data() {
    return {
      isLoading: true,
      page: null,
      pageCount: 1,
      pdfSource:
        '../../public/MAE.pdf',
      showAllPages: true
    }
  },
  watch: {
    showAllPages() {
      this.page = this.showAllPages ? null : 1
    }
  },
  methods: {
    handleDocumentRender(args) {
      console.log(args)
      this.isLoading = false
      this.pageCount = this.$refs.pdfRef.pageCount
    },
    handlePasswordRequest(callback, retry) {
      callback(prompt(retry ? 'Enter password again' : 'Enter password'))
    }
  }
}
</script>
