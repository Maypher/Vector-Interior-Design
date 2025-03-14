<script lang="ts">
	import { websiteUrl } from '$lib/utilities/constants';
	import type { PageData } from './$types';
	import symbol from '$lib/images/symbol.svg';
	import mdToHtml from '$lib/utilities/markdown';
	import '$lib/styles/markdown.css';
	import { getI18n } from '$lib/i18n';
	import Head from '$lib/components/Head.svelte';
	import { page } from '$app/state';

	const { data }: { data: PageData } = $props();
	const sculptures = data.sculptures;

	const i18n = getI18n();

	let groupedSculptures = $derived.by(() => {
		let newImages = [];
		let imageIndex = 0;

		// Iterates over the images.
		// Done in a while loop because the image can be advanced from another while loop within
		// and this one should continue where the inner one leaves off.
		while (imageIndex <= sculptures.length - 1) {
			const image = sculptures[imageIndex];

			// If the image has a group alignment it's the start of a group
			if (image.desktopConfig.groupAlignment) {
				let currentImage = image;
				let imagesGroup = [];

				// Continue fetching images until an image is no longer part of a group.
				// That marks the end of the group.
				while (currentImage?.desktopConfig.groupAlignment) {
					imagesGroup.push(currentImage);
					imageIndex++;

					// A group can be forced to break at a given image.
					// Used make multiple consecutive groups.
					if (currentImage?.desktopConfig.groupEnd) break;

					currentImage = sculptures[imageIndex];
				}

				// Add the new group to the spaces
				newImages.push(imagesGroup);
			} else {
				// Just add the regular image
				newImages.push(image);
				imageIndex++;
			}
		}

		return newImages;
	});
</script>

<Head
	title={$i18n.language === 'es' ? 'Esculturas' : 'Sculptures'}
	description={$i18n.language === 'es' ? '' : ''}
	url={page.url.toString()}
	alternateEn={`${websiteUrl}/en/esculturas`}
	alternateEs={`${websiteUrl}/es/esculturas`}
	ogTitle={$i18n.language === 'es'
		? 'Vector: Interior Design (Esculturas)'
		: 'Vector: Interior Design (Sculptures)'}
	ogDescription={$i18n.language === 'es' ? '' : ''}
	imageUrl={sculptures.at(0)?.imageUrl}
/>

{#snippet desktopImageDescription(description: string, moveToTop: boolean = false)}
	<div class="markdownDescription font-Nexa [&_em]:text-vector-orange w-fit">
		{@html mdToHtml(description)}
	</div>
{/snippet}

<div>
	<div class="lg:hidden">
		{#each sculptures as image, i (image.filename)}
			{@const lastImage = i === sculptures.length - 1}
			<div
				class={`${i === 0 ? 'mt-20' : !lastImage ? 'my-50' : 'my-12'} flex flex-col items-center justify-around gap-10`}
			>
				<img
					src={image.imageUrl}
					alt={image.altTextEs}
					class="w-9/10 max-h-[90svh] object-contain"
				/>
				{#if image.sculptureData.description}
					<div
						class="border-b-vector-orange mx-auto flex w-3/4 flex-col justify-between gap-10 border-b-2 pb-4"
					>
						<img src={symbol} alt="Logo" class="size-28 self-end" />
						<div class="flex items-end justify-between">
							<div class="markdownDescription self-start text-white">
								{@html mdToHtml(image.sculptureData.description)}
							</div>
							{#if lastImage}
								<button
									class="to-top text-vector-grey whitespace-pre-wrap text-3xl hover:cursor-pointer"
									onclick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
								>
									^
								</button>
							{/if}
						</div>
					</div>
				{/if}
			</div>
		{/each}
	</div>
	<div class="bg-vector-grey hidden lg:block">
		{#each groupedSculptures as sculpture, i}
			{#if Array.isArray(sculpture)}
				{@const finalImage = sculpture.at(-1)}
				<figure
					class={`${i === 0 ? 'h-[calc(100vh-5rem)]' : 'h-screen'} flex items-center justify-center gap-20`}
					class:mb-50={i < groupedSculptures.length - 1}
				>
					<div class="flex h-4/5 justify-center gap-20">
						{#each sculpture as sculptureGroup}
							<img
								src={sculptureGroup.imageUrl}
								alt={sculptureGroup.altTextEs}
								class="h-full w-auto"
							/>
						{/each}
					</div>
					{#if finalImage.sculptureData.description}
						<figcaption>
							{@render desktopImageDescription(
								finalImage.sculptureData.description,
								i === groupedSculptures.length - 1
							)}
						</figcaption>
					{/if}
				</figure>
			{:else}
				<figure
					class={`mx-auto flex h-[calc(100vh-5rem)] items-center justify-center gap-20 ${i === 0 ? 'h-[calc(100vh-6rem)]' : 'h-screen'}`}
				>
					<img src={sculpture.imageUrl} alt={sculpture.altTextEs} class="max-h-4/5 h-4/5 w-auto" />
					{#if sculpture.sculptureData.description}
						<figcaption>
							{@render desktopImageDescription(
								sculpture.sculptureData.description,
								i === groupedSculptures.length - 1
							)}
						</figcaption>
					{/if}
				</figure>
			{/if}
		{/each}
	</div>
</div>

<style>
	.to-top {
		animation: to-top 1s ease infinite both;
		position: relative;
	}

	@keyframes to-top {
		0% {
			scale: 1;
		}
		50% {
			scale: 2;
		}
		0% {
			scale: 1;
		}
	}
</style>
