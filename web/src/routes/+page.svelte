<script lang="ts">
	import { invalidateAll, goto } from '$app/navigation';
  import { clean } from '$lib/clean';
  export let data;

  let revealed = false;
  $: trivium = data.trivium;


  function reveal() {
    revealed = true;
  }

  async function next() {
    revealed = false;
    await invalidateAll();
  }

  async function explain() {
    await goto(`/explain/${trivium.id}`);
  }


</script>

<div class="flex p-12 flex-col space-y-4 h-screen">
  <div class="text-m text-slate-400 dark:text-slate-600 self-center">{clean(trivium.category)} - ${trivium.score}</div>
  <div class="text-4xl text-slate-900 dark:text-slate-100 text-center">{clean(trivium.answer)}</div>
  {#if revealed}
    <div class="text-xl text-slate-500 dark:text-slate-400 self-center !my-auto">{clean(trivium.question)}</div>
  {/if}
  <div class="!mt-auto self-center">
  {#if revealed}
    <button on:click={next} class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded text-2xl">next</button>
    <button on:click={explain} class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded text-2xl">explain</button>
  {:else}
    <button on:click={reveal} class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded text-2xl">reveal</button>
  {/if}
</div>

</div>