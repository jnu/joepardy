<script lang="ts">
    import { markdown } from '$lib/markdown';
    import Sanitize from './Sanitize.svelte';
  
    export let content = '';
  </script>
  
  <div class="markdown max-w-full">
    <Sanitize html={markdown(content)} />
  </div>
  