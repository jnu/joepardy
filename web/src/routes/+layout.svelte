<script lang="ts">
  import { navigating } from '$app/stores';
</script>

{#if $navigating}
  <div class="fixed inset-0 flex items-center justify-center bg-slate-100 bg-opacity-70 z-50">
    <div class="animate-ping rounded-full h-16 w-16 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>
  </div>
{/if}
<slot />