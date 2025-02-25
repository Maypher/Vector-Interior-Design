<script lang="ts">
	import type { PageData } from './$types';
	import logo from '$lib/images/logo.svg';
	import { PUBLIC_imagesUrl } from '$env/static/public';
	import '$lib/styles/markdown.css';
	import mdToHtml from '$lib/utilities/markdown';
	import * as enums from '$lib/utilities/enums';
	import symbol from '$lib/images/symbol.svg';
	import { getI18n } from '$lib/i18n';

	const { data }: { data: PageData } = $props();
	const projectData = data.projectData;
	const finalProject = data.finalProject;

	let groupedImageData = $derived.by(() => {
		let newSpaces = [];

		for (const space of projectData.spaces) {
			let updatedImages = [];
			let imageIndex = 0;

			// Iterates over the images.
			// Done in a while loop because the image can be advanced from another while loop within
			// and this one should continue where the inner one leaves off.
			while (imageIndex <= space.images.length - 1) {
				const image = space.images[imageIndex];

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

						currentImage = space.images[imageIndex];
					}

					// Add the new group to the spaces
					updatedImages.push(imagesGroup);
				} else {
					// Just add the regular image
					updatedImages.push(image);
					imageIndex++;
				}
			}

			let spaceCopy = { ...$state.snapshot(space), images: null };
			spaceCopy.images = updatedImages;
			newSpaces.push(spaceCopy);
		}

		return newSpaces;
	});

	const i18n = getI18n();
</script>

{#snippet descriptionContainer(description: string, alignment: string, font: string)}
	<div class={`markdownDescription text-white ${alignment} font-${font}`}>
		{@html mdToHtml(description)}
	</div>
{/snippet}

{#snippet desktopImageView(image: any)}
	<div
		class={`mx-auto flex h-full w-fit items-center justify-center gap-10`}
		class:flex-row={image.desktopConfig.descriptionPosition === enums.Directions.E}
		class:flex-row-reverse={image.desktopConfig.descriptionPosition === enums.Directions.W}
		class:flex-col={image.desktopConfig.descriptionPosition === enums.Directions.S}
		class:flex-col-reverse={image.desktopConfig.descriptionPosition === enums.Directions.N}
	>
		<div
			class={`border-vector-orange flex h-full items-center justify-center gap-x-12 ${
				image.desktopConfig.groupAlignment === enums.GroupAlignment.Centro ? 'items-center' : ''
			} ${image.desktopConfig.groupAlignment === enums.GroupAlignment.Arriba ? 'items-start' : ''} ${
				image.desktopConfig.groupAlignment === enums.GroupAlignment.Abajo ? 'items-end' : ''
			} ${image.desktopConfig.imageBorders.n ? 'border-t-2' : ''} ${
				image.desktopConfig.imageBorders.s ? 'border-b-2' : ''
			}`}
			class:flex-row={image.desktopConfig.descriptionPosition === enums.Directions.E}
			class:flex-row-reverse={image.desktopConfig.descriptionPosition === enums.Directions.W}
			class:flex-col={image.desktopConfig.descriptionPosition === enums.Directions.S}
			class:flex-col-reverse={image.desktopConfig.descriptionPosition === enums.Directions.N}
		>
			<div
				class={`flex size-full w-fit items-center ${
					image.desktopConfig.groupAlignment === enums.GroupAlignment.Centro ? 'items-center' : ''
				} ${image.desktopConfig.groupAlignment === enums.GroupAlignment.Arriba ? 'items-start' : ''} ${
					image.desktopConfig.groupAlignment === enums.GroupAlignment.Abajo ? 'items-end' : ''
				}`}
			>
				<img
					src={`${PUBLIC_imagesUrl}${image.filename}`}
					alt={image.altText}
					class={`border-vector-orange w-auto object-cover ${
						image.desktopConfig.imageBorders.e ? 'border-r-2 px-12' : ''
					} ${image.desktopConfig.imageBorders.w ? 'border-l-2 px-12' : ''}`}
					style={`height: calc(${image.desktopConfig.imageSize}/100 * 100%);`}
				/>
			</div>
			{#if image.description && image.desktopConfig.descriptionPosition}
				<div
					class={`max-w-1/2 border-vector-orange relative size-fit ${image.desktopConfig.descriptionBorders.n ? 'border-t-2 pt-5' : ''} ${
						image.desktopConfig.descriptionBorders.s ? 'border-b-2 pb-5' : ''
					} ${image.desktopConfig.descriptionBorders.e ? 'border-r-2 pr-5' : ''} ${
						image.desktopConfig.descriptionBorders.w ? 'border-l-2 pl-5' : ''
					}`}
				>
					<div class={`m-auto size-fit`}>
						{@render descriptionContainer(
							image.description,
							image.desktopConfig.descriptionAlignment,
							image.descriptionFont
						)}
					</div>
				</div>
			{/if}
		</div>
		{#if image.desktopConfig.logoPosition}
			<div class="flex h-1/2 w-fit items-center">
				<img src={symbol} alt="Símbolo" class="h-full" />
			</div>
		{/if}
	</div>
{/snippet}

{#snippet phoneImageView(image: any)}
	<div
		class={`border-vector-orange my-30 gap-12 ${
			image.phoneConfig?.borders?.n && 'pt-30 border-t-2'
		} ${image.phoneConfig?.borders?.s && 'pb-30 border-b-2'} ${
			image.phoneConfig?.borders?.e && 'pr-30 border-r-2'
		} ${image.phoneConfig?.borders?.w && 'pl-30 border-l-2'}`}
		class:mx-8={image.phoneConfig?.alignment !== enums.Alignment.OVERFLOW}
		class:flex={image.phoneConfig?.descriptionPos}
		class:flex-row={image.phoneConfig?.descriptionPos === enums.Directions.W}
		class:flex-row-reverse={image.phoneConfig?.descriptionPos === enums.Directions.E}
		class:flex-col={image.phoneConfig?.descriptionPos === enums.Directions.N}
		class:flex-col-reverse={image.phoneConfig?.descriptionPos === enums.Directions.S}
	>
		{#if image.description && image.phoneConfig.descriptionPos}
			<div class="mx-auto max-w-[90vw]">
				{@render descriptionContainer(
					image.description,
					image.phoneConfig.descriptionAlignment,
					image.descriptionFont
				)}
			</div>
		{/if}
		<img
			src={`${PUBLIC_imagesUrl}${image.filename}`}
			alt={image.altText}
			class={`${[enums.Alignment.RIGHT, enums.Alignment.LEFT].includes(image.phoneConfig?.alignment) ? 'w-4/5' : ''}`}
			class:ml-auto={image.phoneConfig?.alignment === enums.Alignment.RIGHT}
			class:mr-auto={image.phoneConfig?.alignment === enums.Alignment.LEFT}
		/>
	</div>
{/snippet}

<div class="relative min-h-screen bg-black">
	<header class="bg-vector-grey sticky top-0 z-10 h-20 p-4 lg:static">
		<div class="flex h-full items-center justify-center gap-10">
			<a href={`/${$i18n.language}`} class="h-full transition-transform hover:scale-105">
				<img src={logo} alt="Vector: Interior Design" class="h-full" />
			</a>
		</div>
	</header>

	<div class="block pb-1 lg:hidden">
		{#each projectData.spaces.slice(0, 1) as space (space.id)}
			{#each space.images.slice(0, 1) as image (image.filename)}
				<div class="my-20">
					<img
						src={`${PUBLIC_imagesUrl}${image.filename}`}
						alt={image.altText}
						class:px-8={image.phoneConfig.alignment !== enums.Alignment.OVERFLOW}
					/>
					<div class="mx-8 my-12 text-white">
						<h1
							class="font-Agency-FB border-b-vector-orange my-2 border-b-2 pb-2 indent-1 text-3xl"
						>
							{projectData.name}
						</h1>
						<p class="font-Arial text-right text-sm">Área: {projectData.area} metros cuadrados</p>
						<div class="white markdownDescription my-6 text-justify">
							{@html mdToHtml(projectData.description)}
						</div>
					</div>
				</div>
			{/each}
			{#each space.images.slice(1) as image (image.filename)}
				{@render phoneImageView(image)}
			{/each}
		{/each}

		<div>
			{#each projectData.spaces.slice(1) as space (space.id)}
				{#each space.images as image (image.filename)}
					{@render phoneImageView(image)}
				{/each}
			{/each}
		</div>
	</div>
	<div class="hidden text-white lg:block">
		{#each groupedImageData.slice(0, 1) as space (space.id)}
			{#each space.images.slice(0, 1) as image}
				<div class="p-15 flex h-[calc(100vh-5rem)] w-full items-center justify-evenly gap-5">
					<img
						src={`${PUBLIC_imagesUrl}${image.filename}`}
						alt={image.altText}
						class={`border-vector-orange object-cover ${
							image.desktopConfig.imageBorders.e ? 'border-r-2 px-12' : ''
						} ${image.desktopConfig.imageBorders.w ? 'border-l-2 px-12' : ''}`}
						style={`height: calc(${image.desktopConfig.imageSize}/100 * 100%);`}
					/>
					<div class="max-w-1/2 flex size-full flex-col gap-y-5 p-4 pb-0">
						<div class="border-vector-orange flex w-full justify-between border-b-2 px-4 pb-2">
							<h1 class="font-Agency-FB text-4xl text-white">
								{projectData.name}
							</h1>
							<p class="grow self-end text-right text-white">
								{$i18n.t('area')}: <b>{projectData.area}</b>
								{$i18n.t('areaUnits')}
							</p>
						</div>

						<div class="h-fit shrink-0">
							{@render descriptionContainer(projectData.description, 'text-left', 'Arial')}
						</div>

						{#if Array.isArray(image)}
							<div class="mt-auto flex min-h-0 w-full gap-5">
								{#each image.slice(1) as imageGroup, i (imageGroup.filename)}
									<div class="ml-auto w-fit">
										{@render desktopImageView(imageGroup)}
									</div>
								{/each}
							</div>
						{/if}
					</div>
				</div>
			{/each}
			{#each space.images.slice(1) as image}
				<div class="p-25 flex h-screen justify-center">
					{#if Array.isArray(image)}
						<div class="flex size-full justify-evenly">
							{#each image as groupImage}
								<div class="h-full w-fit">
									{@render desktopImageView(groupImage)}
								</div>
							{/each}
						</div>
					{:else}
						<div class="relative size-full">
							{@render desktopImageView(image)}
						</div>
					{/if}
				</div>
			{/each}
		{/each}
		{#each groupedImageData.slice(1) as space (space.id)}
			{#each space.images as image}
				<div class="p-25 flex h-screen justify-center">
					{#if Array.isArray(image)}
						<div class="flex size-full justify-evenly">
							{#each image as groupImage}
								<div class="h-full w-fit">
									{@render desktopImageView(groupImage)}
								</div>
							{/each}
						</div>
					{:else}
						<div class="size-full">
							{@render desktopImageView(image)}
						</div>
					{/if}
				</div>
			{/each}
		{/each}
	</div>
	<div
		class="-translate-1/2 absolute bottom-0 left-1/2 w-fit text-white transition-transform hover:scale-105"
	>
		<a
			href={finalProject
				? `/${$i18n.language}/proyectos/conclusion`
				: `/${$i18n.language}/proyectos`}
			class="font-Agency-FB gradient-background text-3xl text-transparent"
			>Siguiente -&gt;
		</a>
	</div>
</div>

<style>
	.gradient-background {
		background: linear-gradient(
			90deg,
			var(--color-vector-orange),
			var(--color-vector-grey),
			var(--color-vector-orange),
			var(--color-vector-grey)
		);
		background-size: 300% 300%;
		animation: gradient-animation 1s infinite;
		background-clip: text;
	}

	@keyframes gradient-animation {
		0% {
			background-position: 100% 50%;
		}
		100% {
			background-position: 0% 50%;
		}
	}
</style>
