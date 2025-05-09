<script lang="ts">
	import { isEqual, cloneDeep, isArray } from 'lodash-es';
	import type { PageData } from './$types';
	import ConfigButtons from '$lib/components/editor/ConfigButtons.svelte';
	import EditorDescription from '$lib/components/editor/EditorDescription.svelte';
	import '$lib/styles/markdown.css';
	import Movable from '$lib/components/editor/Movable.svelte';
	import { Directions, GroupAlignment } from '$lib/utilities/enums';
	import symbol from '$lib/images/symbol.svg';
	import Borders from '$lib/components/editor/Borders.svelte';
	import graphql from '$lib/utilities/api';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import { success } from '$lib/utilities/toasts';
	import BgColor from '$lib/components/editor/BgColor.svelte';

	const { data }: { data: PageData } = $props();
	let originalProjectData = $state(data.projectData);
	// svelte-ignore state_referenced_locally
	let updatedProjectData = $state($state.snapshot(originalProjectData));

	let groupedImageData = $derived.by(() => {
		let newSpaces = [];

		for (const space of updatedProjectData.spaces) {
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

			let spaceCopy = $state.snapshot(space);
			spaceCopy.images = updatedImages;
			newSpaces.push(spaceCopy);
		}

		return newSpaces;
	});

	let saveEnabled: boolean = $derived(!isEqual(originalProjectData, updatedProjectData));
	let preview: boolean = $state(false);

	async function updateProjectDesktop() {
		const projectMutation = `
			mutation updateProject($projectId: Int!, $nameEs: String, $nameEn: String, $descriptionEs: String, $descriptionEn: String, $area: Int) {
				updateProject(id: $projectId, nameEs: $nameEs, nameEn: $nameEn, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, area: $area) {
					id
					nameEs
					nameEn
					descriptionEs
					descriptionEn
					area
				}
			}
		`;

		// No space mutation because only things that can be changed there are name, description and index
		// and that's done in a different page.

		const imageMutation = `
			mutation updateImage($filename: String!, $descriptionEs: String, $descriptionEn: String, $descriptionFont: String,
			$index: Int, $desktopConfig: DesktopConfigInput, $bgColor: String) {
				updateImage(filename: $filename, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, descriptionFont: $descriptionFont,
				index: $index, desktopConfig: $desktopConfig, bgColor: $bgColor) {
					filename
					imageUrl
					altTextEs
					descriptionEs
					descriptionEn
					descriptionFont
					bgColor
					desktopConfig {
						    groupAlignment
                            groupEnd
                            imageSize
                            imageBorders {
                                n
                                s
                                e
                                w
                            }
                            descriptionPosition
							descriptionAlignment
                            descriptionBorders {
                                n
                                s
                                e
                                w
                            }
                            descriptionLogoPosition
                            logoPosition
                            logoBorders {
                                n
                                s
                                e
                                w
                            }
					}
				}
			}
		`;

		let updatedProject = (
			await graphql(projectMutation, {
				projectId: updatedProjectData.id,
				nameEs: updatedProjectData.nameEs,
				nameEn: updatedProjectData.nameEn,
				descriptionEs: updatedProjectData.descriptionEs,
				descriptionEn: updatedProjectData.descriptionEn,
				area: updatedProjectData.area
			})
		).updateProject;

		updatedProject.spaces = [];

		// Iterate over a zipped array of [updatedSpace, originalSpace]
		for (let [updatedSpace, originalSpace] of updatedProjectData.spaces.map(
			(el: any, index: number) => [el, originalProjectData.spaces[index]]
		)) {
			let updatedImages = [];

			// Get the images that have been moved around
			const originalOrder = originalSpace.images.map((x: any) => x.filename);
			const updatedOrder = updatedSpace.images.map((x: any) => x.filename);
			const ordersToUpdate = getArrayDifference(originalOrder, updatedOrder);

			for (let [i, image] of updatedSpace.images.entries()) {
				// If the images at the same index between updatedImages and originalImages
				// aren't the same, update it in the backend.
				if (!isEqual(image, originalSpace.images[i])) {
					const updatedImage = (
						await graphql(imageMutation, {
							filename: image.filename,
							descriptionEs: image.descriptionEs,
							descriptionEn: image.descriptionEn,
							descriptionFont: image.descriptionFont,
							bgColor: image.bgColor,
							index: ordersToUpdate.find((val) => val.id === image.filename)?.newPos,
							desktopConfig: image.desktopConfig
						})
					).updateImage;

					updatedImages.push(updatedImage);
				} else updatedImages.push(image); // Just push them into the array to keep the order
			}

			// Update the images in the updatedSpace and add them to the updated project
			updatedSpace.images = updatedImages;
			updatedProject.spaces.push($state.snapshot(updatedSpace));
		}

		// Once everything has been updated, update the original and updatedProjectData variables
		originalProjectData = updatedProject;
		updatedProjectData = cloneDeep(updatedProject); // Doing a deep clone because otherwise they would reference the same value
		success('Proyecto actualizado con éxito!');
	}

	let english: boolean = $state(false);
</script>

{#snippet imageEditor(image: any)}
	<figure
		class={`relative gap-y-20 gap-x-12 ${preview ? 'overflow-visible' : 'overflow-scroll p-10'} ${
			preview ? 'w-fit overflow-visible' : 'w-full border-2 border-dashed'
		} flex justify-center items-center`}
		class:flex-row={image.desktopConfig.descriptionPosition === Directions.E}
		class:flex-row-reverse={image.desktopConfig.descriptionPosition === Directions.W}
		class:flex-col={image.desktopConfig.descriptionPosition === Directions.S && !preview}
		class:flex-col-reverse={image.desktopConfig.descriptionPosition === Directions.N && !preview}
		style={`height: ${!preview ? '100%' : `calc(${image.desktopConfig.imageSize}/100 * 100%)`};`}
	>
		{#if !preview}
			<div class="absolute pointer-events-none top-0 w-full flex justify-between z-10">
				<div class="flex flex-wrap bg-gray-600/70 p-1 gap-2 max-w-7/8 pointer-events-auto">
					<button
						class="transition-colors hover:bg-gray-600/70 cursor-pointer p-2"
						onclick={() => {
							if (image.desktopConfig.descriptionPosition)
								image.desktopConfig.descriptionPosition = null;
							else image.desktopConfig.descriptionPosition = Directions.E;
						}}
					>
						<span class="material-symbols-outlined">
							{image.desktopConfig.descriptionPosition ? 'close' : 'description'}
						</span>
					</button>
					<button
						class="transition-colors hover:bg-gray-600/70 cursor-pointer p-2"
						onclick={() => {
							if (image.desktopConfig.logoPosition) image.desktopConfig.logoPosition = null;
							else image.desktopConfig.logoPosition = Directions.E;
						}}
					>
						<span class="material-symbols-outlined">
							<img src={symbol} alt="Símbolo" class="size-8" />
						</span>
					</button>
					<BgColor bind:color={image.bgColor} imageId={image.filename} />
					<span class="flex items-center w-fit gap-1">
						<label for={`image-size-${image.filename}`}
							>Tamaño de imagen (<input
								type="number"
								bind:value={image.desktopConfig.imageSize}
								min="0"
								max="100"
								class="w-12"
							/>%)
						</label>
						<input
							type="range"
							min="0"
							max="100"
							step="10"
							id={`image-size-${image.filename}`}
							bind:value={image.desktopConfig.imageSize}
						/>
					</span>
					{#if image.desktopConfig.groupAlignment}
						<span class="flex gap-1 items-center">
							<label for={`group-alignment-${image.filename}`}>Alineación:</label>
							<select
								id={`group-alignment-${image.filename}`}
								class="bg-gray-400 p-1 rounded-sm"
								bind:value={image.desktopConfig.groupAlignment}
							>
								{#each Object.entries(GroupAlignment) as [key, val]}
									<option value={val}>{key}</option>
								{/each}
							</select>
						</span>
					{/if}
				</div>
				<div class="absolute top-0 right-0 z-10 flex items-center pointer-events-auto">
					{#if image.desktopConfig.groupAlignment}
						<input
							type="checkbox"
							id={`group-end-${image.filename}`}
							hidden
							bind:checked={image.desktopConfig.groupEnd}
						/>
						<label
							for={`group-end-${image.filename}`}
							class="transition-colors p-2 flex items-center hover:bg-gray-600/70"
						>
							<span
								class="material-symbols-outlined transition-colors"
								class:text-red-500={image.desktopConfig.groupEnd}
							>
								block
							</span>
						</label>
					{/if}
					<button
						class="transition-colors hover:bg-gray-600/70 cursor-pointer p-2 flex justify-center items-center"
						title={image.desktopConfig.groupAlignment
							? 'Remover de grupo'
							: 'Agrupar con superior.'}
						onclick={() => {
							if (image.desktopConfig.groupAlignment) image.desktopConfig.groupAlignment = null;
							else image.desktopConfig.groupAlignment = GroupAlignment.Centro;
						}}
					>
						<span class="material-symbols-outlined">
							{image.desktopConfig.groupAlignment ? 'ad_group_off' : 'ad_group'}
						</span>
					</button>
				</div>
			</div>
		{/if}

		<Borders
			id={image.filename}
			bind:n={image.desktopConfig.imageBorders.n}
			bind:s={image.desktopConfig.imageBorders.s}
			bind:e={image.desktopConfig.imageBorders.e}
			bind:w={image.desktopConfig.imageBorders.w}
			bind:preview
			class={`${!preview ? 'h-9/10' : 'h-full'} w-fit flex items-center`}
		>
			<img
				src={image.imageUrl}
				alt={image.altTextEs}
				class={`object-cover border-vector-orange ${
					image.desktopConfig.imageBorders.e && preview ? 'border-r-2 px-12' : ''
				} ${image.desktopConfig.imageBorders.w && preview ? 'border-l-2 px-12' : ''}`}
				style={`height: ${preview ? '100%' : `calc(${image.desktopConfig.imageSize}/100 * 100%)`};`}
			/>
		</Borders>
		{#if image.desktopConfig.descriptionPosition}
			{@const descTopOrBottom = [Directions.N, Directions.S].includes(
				image.desktopConfig.descriptionPosition
			)}
			<figcaption
				class={`${descTopOrBottom && preview ? 'max-w-9/10 absolute' : preview ? 'max-w-2/5' : ''} ${
					image.desktopConfig.descriptionPosition === Directions.S && preview
						? '-bottom-5 translate-y-full'
						: ''
				} ${image.desktopConfig.descriptionPosition === Directions.N && preview ? '-top-5 -translate-y-full' : ''}`}
			>
				<Borders
					id={`description-${image.filename}`}
					bind:n={image.desktopConfig.descriptionBorders.n}
					bind:s={image.desktopConfig.descriptionBorders.s}
					bind:e={image.desktopConfig.descriptionBorders.e}
					bind:w={image.desktopConfig.descriptionBorders.w}
					bind:preview
					class={`h-fit border-vector-orange ${
						preview && image.desktopConfig.descriptionBorders.n ? 'border-t-2 pt-5' : ''
					} ${
						preview && image.desktopConfig.descriptionBorders.s ? 'border-b-2 pb-5' : ''
					} ${preview && image.desktopConfig.descriptionBorders.e ? 'border-r-2 pr-5' : ''} ${
						preview && image.desktopConfig.descriptionBorders.w ? 'border-l-2 pl-5' : ''
					}`}
				>
					<Movable
						class="size-full text-balance"
						up={image.desktopConfig.descriptionPosition !== Directions.N
							? () => (image.desktopConfig.descriptionPosition = Directions.N)
							: undefined}
						down={image.desktopConfig.descriptionPosition !== Directions.S
							? () => (image.desktopConfig.descriptionPosition = Directions.S)
							: undefined}
						left={image.desktopConfig.descriptionPosition !== Directions.W
							? () => (image.desktopConfig.descriptionPosition = Directions.W)
							: undefined}
						right={image.desktopConfig.descriptionPosition !== Directions.E
							? () => (image.desktopConfig.descriptionPosition = Directions.E)
							: undefined}
						bind:preview
					>
						<EditorDescription
							id={`description-${image.filename}`}
							bind:descriptionEs={image.descriptionEs}
							bind:descriptionEn={image.descriptionEn}
							bind:descriptionFont={image.descriptionFont}
							bind:descriptionAlignment={image.desktopConfig.descriptionAlignment}
							bind:preview
						/>
					</Movable>
				</Borders>
			</figcaption>
		{/if}
		{#if image.desktopConfig.logoPosition}
			<Movable
				left={image.desktopConfig.logoPosition !== Directions.W
					? () => (image.desktopConfig.logoPosition = Directions.W)
					: undefined}
				right={image.desktopConfig.logoPosition !== Directions.E
					? () => (image.desktopConfig.logoPosition = Directions.E)
					: undefined}
				class="flex items-center h-1/2 w-fit"
				bind:preview
			>
				<img src={symbol} alt="Símbolo" class="h-full" />
			</Movable>
		{/if}
	</figure>
{/snippet}

<div class="bg-black text-white hidden xl:block">
	<ConfigButtons
		{saveEnabled}
		bind:preview
		onSaveClick={updateProjectDesktop}
		onCancelClick={() => (updatedProjectData = $state.snapshot(originalProjectData))}
	/>

	{#each groupedImageData.slice(0, 1) as space, spaceIndex (space.id)}
		{@const flatSpace = updatedProjectData.spaces[spaceIndex]}
		{@const moveImage = (fromIndex: number, up: boolean = false) => {
			const image = flatSpace.images.at(fromIndex);
			if (image) {
				flatSpace.images.splice(fromIndex, 1);
				flatSpace.images.splice(fromIndex + (up ? -1 : 1), 0, image);
			}
		}}

		{#each space.images.slice(0, 1) as image}
			{@const isGroup = Array.isArray(image)}
			<div
				class="header-screen py-15 flex justify-evenly items-center transition-colors"
				style={`background-color: ${isGroup ? image.at(-1).bgColor : image.bgColor}`}
			>
				<div class={`${preview ? 'w-fit' : 'w-1/2 border-2 border-dashed'} h-full`}>
					{#if isGroup}
						{@render imageEditor(image[0])}
					{:else}
						{@render imageEditor(image)}
					{/if}
				</div>
				<div class="max-w-2/5">
					<div class="w-full flex justify-between">
						{#if !preview}
							<div class="flex justify-between w-full font-Nexa gap-x-3">
								<div class="flex items-center justify-start gap-2 text-vector-cream">
									{#if english}
										<input
											type="text"
											bind:value={updatedProjectData.nameEn}
											class="text-4xl w-64"
											id="project-name"
										/>
									{:else}
										<input
											type="text"
											bind:value={updatedProjectData.nameEs}
											class="text-4xl w-64"
											id="project-name"
										/>
									{/if}
									<label for="project-name">
										<span
											class="material-symbols-outlined transition-colors hover:bg-gray-700 rounded-md p-1"
										>
											edit
										</span>
									</label>
									<input type="checkbox" id="language" hidden bind:checked={english} />
									<label
										for="language"
										class="p-1 text-xl rounded-sm bg-vector-cream text-vector-black border-2 border-vector-black"
										>{english ? 'Ingles' : 'Español'}
									</label>
								</div>
								<p>
									Área: <input
										type="number"
										class="w-18 border-dashed border-2 border-white p-1"
										bind:value={updatedProjectData.area}
									/>
									m²
								</p>
							</div>
						{:else}
							<div class="font-Nexa text-vector-cream flex w-full flex-col flex-wrap gap-y-20">
								<p
									class="after:bg-vector-orange w-full text-right text-sm after:ml-2 after:mr-20 after:inline-block after:h-2 after:w-8"
								>
									Área: {updatedProjectData.area} m²
								</p>
								<h1 class="block text-4xl">
									{english ? updatedProjectData.nameEn : updatedProjectData.nameEs}
								</h1>
							</div>
						{/if}
					</div>

					<div class="h-fit shrink-0 my-5 font-Nexa text-balance">
						<EditorDescription
							id="project-description"
							bind:descriptionEs={updatedProjectData.descriptionEs}
							bind:descriptionEn={updatedProjectData.descriptionEn}
							bind:preview
						/>
					</div>

					{#if isGroup}
						<div class="w-full flex gap-5 min-h-0 mt-auto">
							{#each image.slice(1) as imageGroup, i (imageGroup.filename)}
								<Movable left={() => moveImage(i)} bind:preview class="w-fit! ml-auto">
									{@render imageEditor(imageGroup)}
								</Movable>
							{/each}
						</div>
					{/if}
				</div>
			</div>
		{/each}
		{#each space.images.slice(1) as image, imageIndex}
			{@const isGroup = Array.isArray(image)}
			<div
				class="h-lvh py-25 flex justify-center transition-colors"
				style={`background-color: ${isGroup ? image.at(-1).bgColor : image.bgColor};`}
			>
				{#if isGroup}
					<div class="size-full flex justify-evenly">
						{#each image as groupImage, groupIndex}
							<!--This is done because it needs to be transformed from the grouped space to the flat space-->
							{@const totalIndex = imageIndex + groupIndex}
							<Movable
								right={groupIndex < image.length - 1
									? () => moveImage(totalIndex, false)
									: undefined}
								left={groupIndex > 0 ? () => moveImage(totalIndex, true) : undefined}
								bind:preview
								class={`h-full ${preview ? 'w-fit' : 'w-full'} flex ${
									groupImage.desktopConfig.groupAlignment === GroupAlignment.Arriba
										? 'items-start'
										: groupImage.desktopConfig.groupAlignment === GroupAlignment.Centro
											? 'items-center'
											: groupImage.desktopConfig.groupAlignment === GroupAlignment.Abajo
												? 'items-end'
												: ''
								}`}
							>
								{@render imageEditor(groupImage)}
							</Movable>
						{/each}
					</div>
				{:else}
					<div class={`h-full ${preview ? 'w-fit' : 'w-full'} flex items-center justify-center`}>
						{@render imageEditor(image)}
					</div>
				{/if}
			</div>
			{#if !preview}
				<hr class="border-t-2 border-dashed border-vector-orange" />
			{/if}
		{/each}
	{/each}
	{#each groupedImageData.slice(1) as space, spaceIndex (space.id)}
		{@const flatSpace = updatedProjectData.spaces[spaceIndex + 1]}
		{@const moveImage = (fromIndex: number, up: boolean = false) => {
			const image = flatSpace.images.at(fromIndex);
			const moveBy = up ? -1 : 1;

			let moveTo = fromIndex + moveBy;
			if (moveTo < 0) moveTo = 0;

			if (image) {
				flatSpace.images.splice(fromIndex, 1);
				flatSpace.images.splice(moveTo, 0, image);
			}
		}}
		{#each space.images as image, imageIndex}
			{@const isGroup = Array.isArray(image)}
			<div
				class="h-lvh py-25 flex justify-center transition-colors"
				style={`background-color: ${isGroup ? image.at(-1).bgColor : image.bgColor};`}
			>
				{#if isGroup}
					<div class="size-full flex justify-evenly">
						{#each image as groupImage, groupIndex}
							<!--This is done because it needs to be transformed from the grouped space to the flat space-->
							{@const totalIndex = imageIndex + groupIndex}
							<Movable
								right={groupIndex < image.length - 1 ? () => moveImage(totalIndex) : undefined}
								left={groupIndex > 0 ? () => moveImage(totalIndex, true) : undefined}
								bind:preview
								class={`h-full ${preview ? 'w-fit' : 'w-full'} flex ${
									groupImage.desktopConfig.groupAlignment === GroupAlignment.Arriba
										? 'items-start'
										: groupImage.desktopConfig.groupAlignment === GroupAlignment.Centro
											? 'items-center'
											: groupImage.desktopConfig.groupAlignment === GroupAlignment.Abajo
												? 'items-end'
												: ''
								}`}
							>
								{@render imageEditor(groupImage)}
							</Movable>
						{/each}
					</div>
				{:else}
					<div class={`h-full ${preview ? 'w-fit' : 'w-full'} flex items-center justify-center`}>
						{@render imageEditor(image)}
					</div>
				{/if}
			</div>
		{/each}
		{#if !preview}
			<hr class="border-t-2 border-dashed border-vector-orange" />
		{/if}
	{/each}
</div>

<div class="xl:hidden">Dispositivo muy pequeño para mostrar este contenido.</div>
