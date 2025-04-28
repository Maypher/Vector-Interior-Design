<script lang="ts">
	import Head from '$lib/components/Head.svelte';
	import { websiteUrl } from '$lib/utilities/constants';
	import type { PageData } from './$types';
	import '$lib/styles/markdown.css';
	import mdToHtml from '$lib/utilities/markdown';
	import * as enums from '$lib/utilities/enums';
	import symbol from '$lib/images/symbol.svg';
	import { getI18n } from '$lib/i18n';
	import { page } from '$app/state';
	import '$lib/styles/skeleton.css';
	import ProjectSectionSkeleton from '$lib/components/ProjectSectionSkeleton.svelte';

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

	let loadedMainImageDesktop: boolean = $state(false);
	let loadedMainImageMobile: boolean = $state(false);
</script>

<Head
	title={projectData.name}
	description={projectData.description}
	url={page.url.toString()}
	alternateEn={`${websiteUrl}/en/proyectos/${projectData.id}`}
	alternateEs={`${websiteUrl}/es/proyectos/${projectData.id}`}
	ogTitle={`Vector: Interior Design (${projectData.name})`}
	ogDescription={projectData.description}
	imageUrl={projectData.thumbnail.imageUrl}
/>

{#snippet descriptionContainer(description: string, alignment: string, font: string)}
	<div class={`markdownDescription ${alignment} font-${font} size-full text-balance`}>
		{@html mdToHtml(description)}
	</div>
{/snippet}

{#snippet desktopImageView(image: any)}
	{@const hasDescription = image.description && image.desktopConfig.descriptionPosition}
	{@const descTopOrBottom = [enums.Directions.N, enums.Directions.S].includes(
		image.desktopConfig.descriptionPosition
	)}
	<div
		class={`mx-auto flex h-full w-fit items-center justify-center gap-10`}
		class:flex-row={image.desktopConfig.descriptionPosition === enums.Directions.E}
		class:flex-row-reverse={image.desktopConfig.descriptionPosition === enums.Directions.W}
		class:flex-col={image.desktopConfig.descriptionPosition === enums.Directions.S}
		class:flex-col-reverse={image.desktopConfig.descriptionPosition === enums.Directions.N}
	>
		<figure
			class={`border-vector-orange relative flex size-full items-center justify-center gap-x-12 ${
				image.desktopConfig.groupAlignment === enums.GroupAlignment.Centro ? 'items-center' : ''
			} ${image.desktopConfig.groupAlignment === enums.GroupAlignment.Arriba ? 'items-start' : ''} ${
				image.desktopConfig.groupAlignment === enums.GroupAlignment.Abajo ? 'items-end' : ''
			} ${image.desktopConfig.imageBorders.n ? 'border-t-2' : ''} ${
				image.desktopConfig.imageBorders.s ? 'border-b-2' : ''
			} ${
				image.desktopConfig.groupAlignment === enums.GroupAlignment.Centro ? 'self-center' : ''
			} ${image.desktopConfig.groupAlignment === enums.GroupAlignment.Arriba ? 'self-start' : ''} ${
				image.desktopConfig.groupAlignment === enums.GroupAlignment.Abajo ? 'self-end' : ''
			}`}
			class:flex-row={image.desktopConfig.descriptionPosition === enums.Directions.E}
			class:flex-row-reverse={image.desktopConfig.descriptionPosition === enums.Directions.W}
			class:flex-col={image.desktopConfig.descriptionPosition === enums.Directions.S}
			class:flex-col-reverse={image.desktopConfig.descriptionPosition === enums.Directions.N}
			style={`height: calc(${image.desktopConfig.imageSize}/100 * 100%);`}
		>
			<img
				src={image.imageUrl}
				alt={image.altText}
				class={`border-vector-orange h-full w-auto object-contain ${
					image.desktopConfig.imageBorders.e ? 'border-r-2 px-12' : ''
				} ${image.desktopConfig.imageBorders.w ? 'border-l-2 px-12' : ''} `}
			/>
			{#if hasDescription}
				<figcaption
					class={`border-vector-orange  ${
						image.desktopConfig.descriptionPosition === enums.Directions.N
							? '-top-5 -translate-y-full'
							: image.desktopConfig.descriptionPosition === enums.Directions.S
								? '-bottom-5 translate-y-full'
								: ''
					} ${
						descTopOrBottom ? 'max-w-9/10 absolute' : 'max-w-2/5'
					} ${image.desktopConfig.descriptionBorders.n ? 'border-t-2 pt-5' : ''} ${
						image.desktopConfig.descriptionBorders.s ? 'border-b-2 pb-5' : ''
					} ${image.desktopConfig.descriptionBorders.e ? 'border-r-2 pr-5' : ''} ${
						image.desktopConfig.descriptionBorders.w ? 'border-l-2 pl-5' : ''
					}`}
				>
					{@render descriptionContainer(
						image.description,
						image.desktopConfig.descriptionAlignment,
						image.descriptionFont
					)}
				</figcaption>
			{/if}
		</figure>
		{#if image.desktopConfig.logoPosition}
			<div class="flex h-1/2 w-fit items-center">
				<img src={symbol} alt="Símbolo" class="h-full" />
			</div>
		{/if}
	</div>
{/snippet}

{#snippet phoneImageView(image: any)}
	<figure
		class={`border-vector-orange py-15 gap-12 ${
			image.phoneConfig?.borders?.n && 'pt-30 border-t-2'
		} ${image.phoneConfig?.borders?.s && 'pb-30 border-b-2'} ${
			image.phoneConfig?.borders?.e && 'pr-30 border-r'
		} ${image.phoneConfig?.borders?.w && 'pl-30 border-l'}`}
		class:px-8={image.phoneConfig?.alignment !== enums.Alignment.OVERFLOW}
		class:flex={image.phoneConfig?.descriptionPos}
		class:flex-row={image.phoneConfig?.descriptionPos === enums.Directions.W}
		class:flex-row-reverse={image.phoneConfig?.descriptionPos === enums.Directions.E}
		class:flex-col={image.phoneConfig?.descriptionPos === enums.Directions.N}
		class:flex-col-reverse={image.phoneConfig?.descriptionPos === enums.Directions.S}
		style={`background-color: ${image.bgColor};`}
	>
		{#if image.description && image.phoneConfig.descriptionPos}
			<figcaption class="max-w-9/10 mx-auto w-full">
				{@render descriptionContainer(
					image.description,
					image.phoneConfig.descriptionAlignment,
					image.descriptionFont
				)}
			</figcaption>
		{/if}
		<img
			src={image.imageUrl}
			alt={image.altText}
			class={`${[enums.Alignment.RIGHT, enums.Alignment.LEFT].includes(image.phoneConfig?.alignment) ? 'w-4/5' : ''} max-h-[90svh] object-contain`}
			class:ml-auto={image.phoneConfig?.alignment === enums.Alignment.RIGHT}
			class:mr-auto={image.phoneConfig?.alignment === enums.Alignment.LEFT}
			class:mx-auto={image.phoneConfig?.alignment === enums.Alignment.CENTER}
		/>
	</figure>
{/snippet}

<div class="relative min-h-screen">
	<div class="block pb-1 lg:hidden">
		{#each projectData.spaces.slice(0, 1) as space (space.id)}
			{#each space.images.slice(0, 1) as image (image.filename)}
				<figure
					class="flex flex-col justify-evenly gap-y-20 py-20"
					class:hidden={!loadedMainImageMobile}
					style={`background-color: ${image.bgColor};`}
				>
					<img
						src={image.imageUrl}
						alt={image.altText}
						class="max-w-3/4 max-h-160 mx-auto"
						onload={() => (loadedMainImageMobile = true)}
					/>
					<figcaption class="px-8">
						<p
							class="font-Nexa after:bg-vector-orange w-full text-right text-sm after:ml-2 after:inline-block after:h-2 after:w-8 max-md:mb-10 md:after:mr-20"
						>
							{$i18n.t('area')}: {projectData.area} m²
						</p>
						<h1 class="font-Nexa mb-6 text-3xl">
							{projectData.name}
						</h1>
						<div class="markdownDescription font-Nexa text-pretty">
							{@html mdToHtml(projectData.description)}
						</div>
					</figcaption>
				</figure>
				<div
					class="header-screen flex flex-col justify-evenly gap-y-20 py-20"
					class:hidden={loadedMainImageMobile}
					style={`background-color: ${image.bgColor};`}
				>
					<div class="skeleton mx-auto aspect-square w-3/4"></div>
					<div class="w-full px-8">
						<div class="skeleton skeleton-line h-4! w-1/4! ml-auto!"></div>
						<div class="skeleton skeleton-line h-12! w-3/4!"></div>
						<div class="w-full">
							<div class="skeleton skeleton-line w-full"></div>
							<div class="skeleton skeleton-line w-full"></div>
							<div class="skeleton skeleton-line w-full"></div>
							<div class="skeleton skeleton-line w-full"></div>
						</div>
					</div>
				</div>
			{/each}
			{#each space.images.slice(1) as image (image.filename)}
				<ProjectSectionSkeleton {image} />
			{/each}
		{/each}

		<div>
			{#each projectData.spaces.slice(1, -1) as space (space.id)}
				{#each space.images.slice(0) as image (image.filename)}
					<ProjectSectionSkeleton {image} />
				{/each}
			{/each}
		</div>
		<div>
			{#each projectData.spaces.slice(-1) as space (space.id)}
				{#each space.images.slice(0, -1) as image (image.filename)}
					<ProjectSectionSkeleton {image} />
				{/each}
				{#each space.images.slice(-1) as image (image.filename)}
					<div class="pb-25" style={`background-color: ${image.bgColor}`}>
						<ProjectSectionSkeleton {image} />
					</div>
				{/each}
			{/each}
		</div>
	</div>
	<div class="hidden lg:block">
		{#each groupedImageData.slice(0, 1) as space (space.id)}
			{#each space.images.slice(0, 1) as image}
				<figure
					class="py-15 header-screen min-h-120 flex w-full items-center justify-evenly"
					class:hidden={!loadedMainImageDesktop}
					style={`background-color: ${image.bgColor};`}
				>
					<img
						src={image.imageUrl}
						alt={image.altText}
						class={`border-vector-orange min-h-110 object-cover ${
							image.desktopConfig.imageBorders.e ? 'border-r-2 px-12' : ''
						} ${image.desktopConfig.imageBorders.w ? 'border-l-2 px-12' : ''}`}
						style={`height: calc(${image.desktopConfig.imageSize}/100 * 100%);`}
						onload={() => (loadedMainImageDesktop = true)}
					/>
					<figcaption class="max-w-2/5">
						<div class="font-Nexa text-vector-cream flex w-full flex-col flex-wrap gap-y-20">
							<p
								class="after:bg-vector-orange w-full text-right text-sm after:ml-2 after:mr-20 after:inline-block after:h-2 after:w-8"
							>
								{$i18n.t('area')}: {projectData.area} m²
							</p>
							<h1 class="block text-4xl">
								{projectData.name}
							</h1>
						</div>

						<div class="my-5 h-fit shrink-0 grow">
							{@render descriptionContainer(projectData.description, 'text-left', 'Nexa')}
						</div>

						{#if Array.isArray(image)}
							<div class="mt-auto flex min-h-0 w-full gap-5">
								{#each image.slice(1) as imageGroup, i (imageGroup.filename)}
									<div class="size-full px-5" style={`flex-basis: calc(1/${image.length} * 100%);`}>
										<ProjectSectionSkeleton image={imageGroup} />
									</div>
								{/each}
							</div>
						{/if}
					</figcaption>
				</figure>
				<div
					class:hidden={loadedMainImageDesktop}
					class="header-screen py-15 min-h-120 flex w-full items-center justify-evenly"
					style={`background-color: ${image.bgColor};`}
				>
					<div class="skeleton aspect-square w-1/3"></div>
					<div class="w-2/5">
						<div class="flex w-full flex-col flex-wrap gap-y-20">
							<div
								class="skeleton skeleton-line w-1/3 self-end text-right text-sm after:ml-2 after:mr-20 after:inline-block after:h-2 after:w-8"
							></div>
							<div class="h-12! skeleton skeleton-line block"></div>
						</div>

						<div class="my-5 h-fit shrink-0 grow">
							<div class="skeleton skeleton-line w-2/3!"></div>
							<div class="skeleton skeleton-line w-2/3!"></div>
							<div class="skeleton skeleton-line w-2/3!"></div>
						</div>
					</div>
				</div>
			{/each}
			{#each space.images.slice(1) as image}
				{@const isGroup = Array.isArray(image)}
				<div
					class="py-25 min-h-120 flex h-lvh justify-center"
					style={`background-color: ${isGroup ? image.at(-1).bgColor : image.bgColor};`}
				>
					{#if isGroup}
						<div class="flex size-full justify-evenly">
							{#each image as groupImage}
								<div class="size-full px-5" style={`flex-basis: calc(1/${image.length} * 100%);`}>
									<ProjectSectionSkeleton image={groupImage} />
								</div>
							{/each}
						</div>
					{:else}
						<div class="relative size-full">
							<ProjectSectionSkeleton {image} />
						</div>
					{/if}
				</div>
			{/each}
		{/each}
		{#each groupedImageData.slice(1) as space (space.id)}
			{#each space.images as image}
				{@const isGroup = Array.isArray(image)}
				<div
					class="py-25 min-h-120 flex h-lvh justify-center"
					style={`background-color: ${isGroup ? image.at(-1).bgColor : image.bgColor};`}
				>
					{#if isGroup}
						<div class="flex size-full justify-evenly">
							{#each image as groupImage}
								<div class="size-full px-5" style={`flex-basis: calc(1/${image.length} * 100%);`}>
									<ProjectSectionSkeleton image={groupImage} />
								</div>
							{/each}
						</div>
					{:else}
						<div class="size-full">
							<ProjectSectionSkeleton {image} />
						</div>
					{/if}
				</div>
			{/each}
		{/each}
	</div>
	<div
		class="hover:scale-120 absolute bottom-10 left-1/2 w-fit -translate-x-1/2 transition-transform lg:bottom-5"
	>
		<a
			href={finalProject
				? `/${$i18n.language}/proyectos/conclusion`
				: `/${$i18n.language}/proyectos/#${data.nextProjectId}`}
			class="font-Nexa gradient-background text-vector-cream h-fit text-6xl font-extrabold"
			aria-label={$i18n.language === 'es' ? 'siguiente' : 'next'}
		>
			<div id="arrow">&gt;</div>
		</a>
	</div>
</div>

<style>
	#arrow {
		animation: 1s ease-in-out infinite both alternate move-arrow;
	}

	@keyframes move-arrow {
		to {
			transform: translateX(1rem);
		}
	}
</style>
