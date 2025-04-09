<script lang="ts">
	import { websiteUrl } from '$lib/utilities/constants';
	import type { PageData } from './$types';
	import whiteLogo from '$lib/images/logo white.svg';
	import mdToHtml from '$lib/utilities/markdown';
	import '$lib/styles/markdown.css';
	import { getI18n } from '$lib/i18n';
	import Head from '$lib/components/Head.svelte';
	import { page } from '$app/state';
	import { scrollToTop } from '$lib/utilities/navigation';
	import SculptureSkeleton from '$lib/components/SculptureSkeleton.svelte';

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
	ogDescription={$i18n.language === 'es' ? 'Esculturas' : 'Sculptures'}
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
			<div
				class={`${i === 0 ? 'header-screen' : 'h-svh'}`}
				style={`background-color: ${image.sculptureData.bgColor};`}
			>
				<SculptureSkeleton {image} />
			</div>
		{/each}
		<button
			onclick={scrollToTop}
			class="hover:scale-120 relative bottom-5 mx-auto block cursor-pointer transition-transform"
		>
			<img src={whiteLogo} alt="Vector: Interior Design" class="h-10" />
		</button>
	</div>
	<div class="relative hidden lg:block">
		{#each groupedSculptures as sculpture, i}
			{#if Array.isArray(sculpture)}
				{@const finalImage = sculpture.at(-1)}
				<figure
					class={`${i === 0 ? 'header-screen' : 'h-screen'} flex items-center justify-center gap-20`}
					class:mb-50={i < groupedSculptures.length - 1}
					style={`background-color: ${sculpture.at(-1).sculptureData.bgColor};`}
				>
					<div class="flex h-4/5 items-center justify-center gap-20">
						{#each sculpture as sculptureGroup, groupIndex}
							{@const groupLength = groupedSculptures.length}
							<div style={`height: calc(${groupLength - groupIndex}/${groupLength} * 90%);`}>
								<SculptureSkeleton image={sculptureGroup} />
							</div>
						{/each}
					</div>
				</figure>
			{:else}
				<div
					class={`${i === 0 ? 'header-screen' : 'h-screen'}`}
					style={`background-color: ${sculpture.sculptureData.bgColor}`}
				>
					<SculptureSkeleton image={sculpture} />
				</div>
			{/if}
		{/each}
		<button
			onclick={scrollToTop}
			class="hover:scale-120 absolute bottom-20 right-20 cursor-pointer transition-transform"
		>
			<img src={whiteLogo} alt="Vector: Interior Design" class="h-10" />
		</button>
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
