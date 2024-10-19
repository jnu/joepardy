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

<div class="flex flex-col h-screen justify-between dark:bg-slate-300">
  <div class="text-m bg-blue-400 dark:bg-blue-300 dark:text-white w-full py-2 text-center">{clean(trivium.category)} - ${trivium.score}</div>
  <div class="text-3xl text-slate-900 dark:text-slate-100 text-center grow-1 overflow-y-auto py-4 px-4">{clean(trivium.answer)}</div>
  {#if revealed}
    <div class="text-3xl text-green-700 self-center !mt-auto">{clean(trivium.question)}</div>
  {/if}
  <div class="!mt-auto self-center w-full">
  {#if revealed}
    <div class="flex w-full">
    <button on:click={next} class="bg-red-500 hover:bg-red-600 dark:text-white font-bold py-4 text-2xl basis-1/2">next</button>
    <button on:click={explain} class="bg-blue-500 hover:bg-blue-600 dark:text-white font-bold py-4 text-2xl basis-1/2">explain</button>
    </div>
  {:else}
    <button on:click={reveal} class="bg-green-400 dark:bg-green-500 hover:bg-green-500 hover:dark:bg-green-600 dark:text-white font-bold w-full text-2xl py-4">reveal</button>
  {/if}
</div>

</div>