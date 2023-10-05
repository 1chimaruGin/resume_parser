<template>
  <div class="footer">
    <span style="text-transform: uppercase"
      >&copy; 2023 <strong>Resume Scanner</strong>. All Rights Reserved.</span
    >
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Footer extends Vue {
}
</script>

<style scoped>
.footer {
  padding: 30px;
  /* background: #ECEFF1; */
  background: #e7eff3;
  text-align: center;
}
</style>
