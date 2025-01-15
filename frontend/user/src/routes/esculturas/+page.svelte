<script lang="ts">
	import type { PageData } from './$types';
	import { PUBLIC_imagesUrl } from '$env/static/public';
	import symbol from '$lib/images/symbol.svg';

	const { data }: { data: PageData } = $props();
	const sculptures = data.sculptures;
</script>

<div>
	{#each sculptures as image}
		<div class="flex min-h-screen flex-col justify-around p-8">
			<img src={`${PUBLIC_imagesUrl}${image.filename}`} alt={image.altText} />
			{#if image.sculptureData.descriptionEs}
				<div class="border-b-vector-orange relative mx-auto w-fit max-w-72 border-b-2 pb-2 pl-10">
					<img src={symbol} alt="Logo" class="absolute -left-7 bottom-1 size-20" />
					<p class="text-right text-2xl text-white">{image.sculptureData.descriptionEs}</p>
				</div>
			{/if}
		</div>
	{/each}
</div>
