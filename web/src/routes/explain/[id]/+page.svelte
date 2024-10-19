<script lang="ts">
	import { goto } from '$app/navigation';
    import {clean} from '$lib/clean';
  export let data;

  $: explanation = data.explanation;


  async function next() {
    await goto(`/`);
  }


</script>

<div class="flex p-12 flex-col space-y-2 h-screen">
    <div class="text-m text-slate-600 dark:text-slate-400 text-center">{clean(explanation.trivium.category)} - ${explanation.trivium.score}</div>
    <div class="text-sm text-slate-400 dark:text-slate-600 self-center">{clean(explanation.trivium.answer)}: <span class="font-bold">{clean(explanation.trivium.question)}</span></div>
  <div class="text-m text-slate-900 dark:text-slate-100 text-left overflow-y-auto"><span class="font-bold">Summary:</span>{explanation.summary.content}</div>
    <div class="!mt-auto self-center">
        <button on:click={next} class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded text-2xl">next</button>
    </div>
</div>