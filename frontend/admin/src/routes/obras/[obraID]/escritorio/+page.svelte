<script lang="ts">
	import { isEqual, cloneDeep } from 'lodash-es';
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
			mutation updateProject($projectId: Int!, $name: String, $descriptionEs: String, $descriptionEn: String, $area: Int) {
				updateProject(id: $projectId, name: $name, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, area: $area) {
					id
					name
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
			$index: Int, $desktopConfig: DesktopConfigInput) {
				updateImage(filename: $filename, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, descriptionFont: $descriptionFont,
				index: $index, desktopConfig: $desktopConfig) {
					filename
					altTextEs
					descriptionEs
					descriptionEn
					descriptionFont
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
				name: updatedProjectData.name,
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
</script>

{#snippet imageEditor(image: any)}
	<div
		class={`relative h-full ${preview ? 'w-fit' : ''} mx-auto flex justify-center items-center gap-10`}
		class:flex-row={image.desktopConfig.logoPosition === Directions.E}
		class:flex-row-reverse={image.desktopConfig.logoPosition === Directions.W}
		class:flex-col={image.desktopConfig.logoPosition === Directions.S}
		class:flex-col-reverse={image.desktopConfig.logoPosition === Directions.N}
	>
		{#if !preview}
			<div class="absolute top-0 w-full flex justify-between z-10">
				<div class="flex flex-wrap bg-gray-600/70 p-1 gap-2 max-w-7/8">
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
				<div class="absolute top-0 right-0 z-10 flex items-center">
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
		<div
			class={`h-full flex items-center justify-center gap-x-12 border-vector-orange ${!preview ? 'gap-y-12' : ''} ${
				image.desktopConfig.groupAlignment === GroupAlignment.Centro ? 'items-center' : ''
			} ${image.desktopConfig.groupAlignment === GroupAlignment.Arriba ? 'items-start' : ''} ${
				image.desktopConfig.groupAlignment === GroupAlignment.Abajo ? 'items-end' : ''
			} ${image.desktopConfig.imageBorders.n && preview ? 'border-t-2' : ''} ${
				image.desktopConfig.imageBorders.s && preview ? 'border-b-2' : ''
			}`}
			class:flex-row={image.desktopConfig.descriptionPosition === Directions.E}
			class:flex-row-reverse={image.desktopConfig.descriptionPosition === Directions.W}
			class:flex-col={image.desktopConfig.descriptionPosition === Directions.S}
			class:flex-col-reverse={image.desktopConfig.descriptionPosition === Directions.N}
		>
			<Borders
				id={image.filename}
				bind:n={image.desktopConfig.imageBorders.n}
				bind:s={image.desktopConfig.imageBorders.s}
				bind:e={image.desktopConfig.imageBorders.e}
				bind:w={image.desktopConfig.imageBorders.w}
				bind:preview
				class={`flex items-center w-fit! ${
					image.desktopConfig.groupAlignment === GroupAlignment.Centro ? 'items-center' : ''
				} ${image.desktopConfig.groupAlignment === GroupAlignment.Arriba ? 'items-start' : ''} ${
					image.desktopConfig.groupAlignment === GroupAlignment.Abajo ? 'items-end' : ''
				}`}
			>
				<img
					src={image.imageUrl}
					alt={image.altTextEs}
					class={`object-cover transition-[height] border-vector-orange ${
						image.desktopConfig.imageBorders.e && preview ? 'border-r-2 px-12' : ''
					} ${image.desktopConfig.imageBorders.w && preview ? 'border-l-2 px-12' : ''}`}
					style={`height: calc(${image.desktopConfig.imageSize}/100 * 100%);`}
				/>
			</Borders>
			{#if image.desktopConfig.descriptionPosition}
				<Borders
					id={`description-${image.filename}`}
					bind:n={image.desktopConfig.descriptionBorders.n}
					bind:s={image.desktopConfig.descriptionBorders.s}
					bind:e={image.desktopConfig.descriptionBorders.e}
					bind:w={image.desktopConfig.descriptionBorders.w}
					bind:preview
					class={`${preview ? 'max-w-1/2 w-fit' : ''} grow h-fit border-vector-orange ${preview && image.desktopConfig.descriptionBorders.n ? 'border-t-2 pt-5' : ''} ${
						preview && image.desktopConfig.descriptionBorders.s ? 'border-b-2 pb-5' : ''
					} ${preview && image.desktopConfig.descriptionBorders.e ? 'border-r-2 pr-5' : ''} ${
						preview && image.desktopConfig.descriptionBorders.w ? 'border-l-2 pl-5' : ''
					}`}
				>
					<Movable
						class={`h-fit ${
							image.desktopConfig.descriptionPosition === Directions.N ? 'absolute top-0' : ''
						} ${image.desktopConfig.descriptionPosition === Directions.S ? 'absolute bottom-0' : ''}`}
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
			{/if}
		</div>
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
	</div>
{/snippet}

<div class="bg-black text-white hidden xl:block">
	<ConfigButtons
		{saveEnabled}
		bind:preview
		onSaveClick={updateProjectDesktop}
		onCancelClick={() => (updatedProjectData = $state.snapshot(originalProjectData))}
	/>

	{#each groupedImageData.slice(0, 1) as space, spaceId (space.id)}
		{@const flatSpace = updatedProjectData.spaces[spaceId]}
		{@const moveImage = (fromIndex: number, up: boolean = false) => {
			const image = flatSpace.images.at(fromIndex);
			if (image) {
				flatSpace.images.splice(fromIndex, 1);
				flatSpace.images.splice(fromIndex + (up ? -1 : 1), 0, image);
			}
		}}

		{#each space.images.slice(0, 1) as image}
			<div class="h-[calc(100vh-5rem)] p-15 flex justify-evenly items-center gap-5">
				<Movable
					down={!Array.isArray(image) ? () => moveImage(0) : undefined}
					right={Array.isArray(image) ? () => moveImage(0) : undefined}
					bind:preview
					class={`${preview ? 'w-fit' : ''}`}
				>
					{#if Array.isArray(image)}
						{@render imageEditor(image[0])}
					{:else}
						{@render imageEditor(image)}
					{/if}
				</Movable>
				<div class="flex flex-col gap-y-5 size-full max-w-1/2 p-4 pb-0">
					<div class="w-full flex justify-between border-vector-orange border-b-2 pb-2 px-4">
						{#if !preview}
							<div class="flex justify-between w-full">
								<div class="flex items-center justify-start gap-2">
									<input
										type="text"
										bind:value={updatedProjectData.name}
										class="text-white font-Agency-FB text-4xl w-64"
										id="project-name"
									/>
									<label for="project-name">
										<span
											class="material-symbols-outlined transition-colors hover:bg-gray-700 rounded-md p-1"
										>
											edit
										</span>
									</label>
								</div>
								<p>
									Área: <input
										type="number"
										class="w-18 border-dashed border-2 border-white p-1 text-white"
										bind:value={updatedProjectData.area}
									/>
									metros cuadrados
								</p>
							</div>
						{:else}
							<h1 class="text-white font-Agency-FB text-4xl">
								{updatedProjectData.name}
							</h1>
							<p class="text-white grow self-end text-right">
								Área: {updatedProjectData.area}
								metros cuadrados
							</p>
						{/if}
					</div>

					<div class="h-fit shrink-0">
						<EditorDescription
							id="project-description"
							bind:descriptionEs={updatedProjectData.descriptionEs}
							bind:descriptionEn={updatedProjectData.descriptionEn}
							descriptionFont={'Arial'}
							bind:preview
						/>
					</div>

					{#if Array.isArray(image)}
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
		{#each space.images.slice(1) as image}
			<div class="h-screen p-25 flex justify-center">
				{#if Array.isArray(image)}
					<div class="size-full flex justify-evenly">
						{#each image as groupImage, groupIndex}
							<Movable
								right={groupIndex < image.length - 1
									? () => {
											const fromIndex = flatSpace.images.indexOf(groupImage);
											flatSpace.images.splice(fromIndex, 1);
											flatSpace.images.splice(fromIndex - 1, 0, groupImage);
										}
									: undefined}
								left={groupIndex > 0
									? () => {
											const fromIndex = flatSpace.images.indexOf(groupImage);

											flatSpace.images.splice(fromIndex, 1);
											flatSpace.images.splice(fromIndex + 1, 0, groupImage);
										}
									: undefined}
								bind:preview
								class={`h-full ${preview ? 'w-fit' : 'w-full'}`}
							>
								{@render imageEditor(groupImage)}
							</Movable>
						{/each}
					</div>
				{:else}
					<Movable
						up={() => {
							const fromIndex: number = flatSpace.images.indexOf(image);

							flatSpace.images.splice(fromIndex, 1);
							flatSpace.images.splice(fromIndex - 1, 0, image);
						}}
						down={() => {
							const fromIndex: number = flatSpace.images.indexOf(image);

							let imageToMove = flatSpace.images[fromIndex];
							flatSpace.images.splice(fromIndex, 1);
							flatSpace.images.splice(fromIndex + 1, 0, imageToMove);
						}}
						bind:preview
						class="size-full relative"
					>
						{@render imageEditor(image)}
					</Movable>
				{/if}
			</div>
			{#if !preview}
				<hr class="border-t-2 border-dashed border-vector-orange" />
			{/if}
		{/each}
	{/each}
	{#each groupedImageData.slice(1) as space, spaceId (space.id)}
		{@const flatSpace = updatedProjectData.spaces[spaceId + 1]}
		{#each space.images as image, i}
			<div class="h-screen p-25 flex justify-center">
				{#if Array.isArray(image)}
					<div class="size-full flex justify-evenly">
						{#each image as groupImage, groupIndex}
							<Movable
								right={groupIndex < image.length - 1
									? () => {
											const fromIndex = flatSpace.images.indexOf(groupImage);
											flatSpace.images.splice(fromIndex, 1);
											flatSpace.images.splice(fromIndex - 1, 0, groupImage);
										}
									: undefined}
								left={groupIndex > 0
									? () => {
											const fromIndex = flatSpace.images.indexOf(groupImage);

											flatSpace.images.splice(fromIndex, 1);
											flatSpace.images.splice(fromIndex + 1, 0, groupImage);
										}
									: undefined}
								bind:preview
								class={`h-full ${preview ? 'w-fit' : 'w-full'}`}
							>
								{@render imageEditor(groupImage)}
							</Movable>
						{/each}
					</div>
				{:else}
					<Movable
						up={i > 0
							? () => {
									const fromIndex = i;

									let image = flatSpace.images[fromIndex];
									flatSpace.images.splice(fromIndex, 1);
									flatSpace.images.splice(fromIndex - 1, 0, image);
								}
							: undefined}
						down={i <= space.images.length - 1
							? () => {
									const fromIndex = i;

									let image = flatSpace.images[fromIndex];
									flatSpace.images.splice(fromIndex, 1);
									flatSpace.images.splice(fromIndex + 1, 0, image);
								}
							: undefined}
						bind:preview
						class="size-full relative"
					>
						{@render imageEditor(image)}
					</Movable>
				{/if}
			</div>
		{/each}
		{#if !preview}
			<hr class="border-t-2 border-dashed border-vector-orange" />
		{/if}
	{/each}
</div>

<div class="xl:hidden">Dispositivo muy pequeño para mostrar este contenido.</div>
