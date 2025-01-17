<script lang="ts">
	import type { PageData } from './$types';
	import { PUBLIC_imagesUrl } from '$env/static/public';
	import symbol from '$lib/images/symbol.svg';
	import mdToHtml from '$lib/utilities/markdown';
	import logo from '$lib/images/logo.svg';
	import '$lib/styles/markdown.css';

	const { data }: { data: PageData } = $props();
	const sculptures = data.sculptures;
</script>

<div>
	<header class="bg-vector-grey flex h-1/5 items-center justify-between p-5">
		<a href="/">
			<img src={logo} alt="" class="m-auto h-fit w-[55%]" id="logo" />
		</a>
	</header>

	{#each sculptures as image, i (image.filename)}
		<div class="my-20 flex flex-col items-center justify-around gap-10">
			<img src={`${PUBLIC_imagesUrl}${image.filename}`} alt={image.altText} class:px-8={i !== 0} />
			{#if image.sculptureData.descriptionEs}
				<div
					class="border-b-vector-orange mx-auto flex w-3/4 flex-col justify-between gap-10 border-b-2 pb-4"
				>
					<img src={symbol} alt="Logo" class="size-28 w-fit self-end" />
					<div class="markdownDescription self-start text-white">
						{@html mdToHtml(image.sculptureData.descriptionEs)}
					</div>
				</div>
			{/if}
		</div>
	{/each}
</div>
