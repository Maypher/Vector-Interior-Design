<script lang="ts">
	import type { PageData } from './$types';
	import { PUBLIC_imagesUrl } from '$env/static/public';
	import symbol from '$lib/images/symbol.svg';
	import mdToHtml from '$lib/utilities/markdown';
	import logo from '$lib/images/logo.svg';
	import '$lib/styles/markdown.css';

	const { data }: { data: PageData } = $props();
	const sculptures = data.sculptures;

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

{#snippet desktopImageDescription(description: string, moveToTop: boolean = false)}
	<div class="border-b-vector-orange mx-auto flex w-3/4 justify-between gap-10 border-b-2 pb-4">
		<div class="markdownDescription self-end text-white">
			{@html mdToHtml(description)}
		</div>
		<div class="flex items-center">
			<img src={symbol} alt="Logo" class="size-28 w-fit self-end" />
			{#if moveToTop}
				<button
					class="to-top text-vector-grey whitespace-pre-wrap text-3xl hover:cursor-pointer"
					onclick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
				>
					^
				</button>
			{/if}
		</div>
	</div>
{/snippet}

<div>
	<header class="bg-vector-grey flex h-20 items-center justify-center gap-10 p-4 md:gap-20">
		<a href="/#nav" class="h-full transition-transform hover:scale-125">
			<img src={logo} alt="Logo" class="h-full" />
		</a>
		<p class="font-Agency-FB text-center text-lg md:text-3xl" style="word-spacing: 0.5 trem;">
			Obras únicas y exclusivas
		</p>
	</header>
	<div class="md:hidden">
		{#each sculptures as image, i (image.filename)}
			{@const lastImage = i === sculptures.length - 1}
			<div
				class={`${i === 0 ? 'mt-20' : !lastImage ? 'my-50' : 'my-2'} flex flex-col items-center justify-around gap-10`}
			>
				<img
					src={`${PUBLIC_imagesUrl}${image.filename}`}
					alt={image.altText}
					class:px-8={i !== 0}
					class="w-full"
				/>
				{#if image.sculptureData.descriptionEs}
					<div
						class="border-b-vector-orange mx-auto flex w-3/4 flex-col justify-between gap-10 border-b-2 pb-4"
					>
						<img src={symbol} alt="Logo" class="size-28 w-fit self-end" />
						<div class="flex items-end justify-between">
							<div class="markdownDescription self-start text-white">
								{@html mdToHtml(image.sculptureData.descriptionEs)}
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
	<div class="hidden md:block">
		{#each groupedSculptures as sculpture, i}
			{#if Array.isArray(sculpture)}
				{@const finalImage = sculpture.at(-1)}
				<div
					class={`mb-50 ${i === 0 ? 'h-[calc(100vh-6rem)]' : 'h-screen'} flex flex-col justify-center`}
					class:mb-50={i < groupedSculptures.length - 1}
				>
					<div class="h-13/20 flex justify-center gap-20">
						{#each sculpture as sculptureGroup}
							<img
								src={`${PUBLIC_imagesUrl}${sculptureGroup.filename}`}
								alt={sculptureGroup.altText}
								class="h-full w-auto"
							/>
						{/each}
					</div>
					{#if finalImage.sculptureData.descriptionEs}
						{@render desktopImageDescription(
							finalImage.sculptureData.descriptionEs,
							i === groupedSculptures.length - 1
						)}
					{/if}
				</div>
			{:else}
				<div
					class={`${i === groupedSculptures.length - 1 ? '' : 'mb-50'}  flex h-[calc(100vh-6rem)] flex-col items-center justify-center ${i === 0 ? 'h-[calc(100vh-6rem)]' : 'h-screen'}`}
				>
					<img
						src={`${PUBLIC_imagesUrl}${sculpture.filename}`}
						alt={sculpture.altText}
						class:px-8={i !== 0}
						class="h-13/20 max-h-4/5 w-auto"
					/>
					{#if sculpture.sculptureData.descriptionEs}
						{@render desktopImageDescription(
							sculpture.sculptureData.descriptionEs,
							i === groupedSculptures.length - 1
						)}
					{/if}
				</div>
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
