<script lang="ts">
	import type { Snippet } from 'svelte';

	const { children }: { children: Snippet } = $props();
</script>

<div
	id="phone"
	class="bg-black md:border-2 mb-20 md:border-white md:aspect-[9/16] w-full md:w-sm flex flex-col overflow-y-scroll overflow-x-clip relative"
>
	<div
		class="bg-black z-30 h-10 shrink-0 md:border-white md:border-2 w-full hidden md:flex sticky top-0 justify-center items-center"
	>
		<div class="size-4 rounded-xl border-2 border-white hidden md:block"></div>
	</div>
	<div class="min-h-0 @container">
		{@render children()}
	</div>
</div>
