<script lang="ts">
	import '$lib/styles/skeleton.css';
	import mdToHtml from '$lib/utilities/markdown';

	const { image }: { image: any } = $props();

	let imgLoadedMobile: boolean = $state(false);
	let imgLoadedDesktop: boolean = $state(false);
</script>

{#snippet descriptionContainer(desc: string, imgLoaded: boolean)}
	<div class="markdownDescription font-Nexa [&_em]:text-vector-orange" class:hidden={!imgLoaded}>
		{@html mdToHtml(desc)}
	</div>
	<div class:hidden={imgLoaded}>
		<div class="skeleton skeleton-line"></div>
		<div class="skeleton skeleton-line"></div>
		<div class="skeleton skeleton-line"></div>
	</div>
{/snippet}

<div class="size-full lg:hidden">
	<div class="flex size-full flex-col items-center justify-evenly" class:hidden={imgLoadedMobile}>
		<div class="w-9/10 skeleton max-h-1/2 mx-auto aspect-square"></div>
		{#if image.sculptureData.description}
			{@render descriptionContainer(image.sculptureData.description, imgLoadedMobile)}
		{/if}
	</div>
	<figure
		class="flex size-full flex-col items-center justify-evenly"
		class:hidden={!imgLoadedMobile}
	>
		<img
			src={image.imageUrl}
			alt={image.altText}
			class="w-9/10 max-h-3/4 object-contain"
			onload={() => (imgLoadedMobile = true)}
		/>
		{#if image.sculptureData.description}
			<figcaption>
				{@render descriptionContainer(image.sculptureData.description, imgLoadedMobile)}
			</figcaption>
		{/if}
	</figure>
</div>

<div class="hidden size-full lg:block">
	<figure
		class="mx-auto flex size-full items-center justify-center gap-20"
		class:hidden={!imgLoadedDesktop}
	>
		<img
			src={image.imageUrl}
			alt={image.altText}
			class="max-h-4/5 h-4/5 w-auto"
			onload={() => (imgLoadedDesktop = true)}
		/>
		{#if image.sculptureData.description}
			<figcaption>
				{@render descriptionContainer(image.sculptureData.description, imgLoadedDesktop)}
			</figcaption>
		{/if}
	</figure>
	<div
		class:hidden={imgLoadedDesktop}
		class="mx-auto flex size-full items-center justify-center gap-20"
	>
		<div class="skeleton aspect-square h-4/5"></div>
		{#if image.sculptureData.description}
			{@render descriptionContainer(image.sculptureData.description, imgLoadedDesktop)}
		{/if}
	</div>
</div>
