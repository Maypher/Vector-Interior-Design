<script lang="ts">
	import Phone from '$lib/components/layout/phone.svelte';
	import type { PageData } from './$types';
	import logo from '$lib/images/logo.svg';
	import { PUBLIC_imageURL } from '$env/static/public';
	import { mdToHTML } from '$lib/utilities/markdown';
	import Borders from '$lib/components/editor/Borders.svelte';
	import Movable from '$lib/components/editor/Movable.svelte';
	import { Alignment, Directions } from '$lib/utilities/enums';
	import EditorDescription from '$lib/components/editor/EditorDescription.svelte';
	import { isEqual, cloneDeep } from 'lodash-es';
	import '$lib/styles/markdown.css';
	import graphql from '$lib/utilities/api';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import { success } from '$lib/utilities/toasts';

	const { data }: { data: PageData } = $props();
	let originalProjectData = $state(data.projectData);
	// svelte-ignore state_referenced_locally
	let updatedProjectData = $state($state.snapshot(originalProjectData));

	let preview: boolean = $state(false);
	let saveEnabled: boolean = $derived(!isEqual(originalProjectData, updatedProjectData));

	async function updateMobileConfig() {
		const projectMutation = `
			mutation updateProject($projectId: Int!, $name: String, $descriptionEs: String!, $descriptionEn: String!, $area: Int) {
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
			$index: Int, $phoneConfig: PhoneConfigInput) {
				updateImage(filename: $filename, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn,
				descriptionFont: $descriptionFont, index: $index, phoneConfig: $phoneConfig) {
					filename
					altTextEs
					descriptionEs
					descriptionEn
					descriptionFont
					phoneConfig {
						borders {
							n
							s
							e
							w
						}
						alignment
						descriptionPos
						descriptionAlignment
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
							descriptionFont: image.descriptionAlignment,
							index: ordersToUpdate.find((val) => val.id === image.filename)?.newPos,
							phoneConfig: image.phoneConfig
						})
					).updateImage;

					updatedImages.push(updatedImage);
				} else updatedImages.push(image); // Just push them into the array to keep the order
			}

			// Update the images in the updatedSpace and add them to the updated project
			updatedSpace.images = updatedImages;
			updatedProject.spaces.push(updatedSpace);
		}

		// Once everything has been updated, update the original and updatedProjectData variables
		originalProjectData = updatedProject;
		updatedProjectData = cloneDeep(updatedProject); // Doing a deep clone because otherwise they would reference the same value
		success('Proyecto actualizado con éxito!');
	}
</script>

{#snippet imageEditor(imageData: any)}
	<div class="size-full">
		{#if !preview}
			<Borders
				id={imageData.filename}
				bind:n={imageData.phoneConfig.borders.n}
				bind:s={imageData.phoneConfig.borders.s}
				bind:e={imageData.phoneConfig.borders.e}
				bind:w={imageData.phoneConfig.borders.w}
				bind:preview
			>
				<div
					class={`border-vector-orange gap-12 ${
						imageData.phoneConfig.alignment !== Alignment.Sangrar ? 'px-8' : ''
					}`}
					class:flex={imageData.phoneConfig.descriptionPos}
					class:flex-row={imageData.phoneConfig.descriptionPos === Directions.W}
					class:flex-row-reverse={imageData.phoneConfig.descriptionPos === Directions.E}
					class:flex-col={imageData.phoneConfig.descriptionPos === Directions.N}
					class:flex-col-reverse={imageData.phoneConfig.descriptionPos === Directions.S}
				>
					{#if imageData.phoneConfig.descriptionPos}
						<Movable
							up={imageData.phoneConfig.descriptionPos !== Directions.N
								? () => (imageData.phoneConfig.descriptionPos = Directions.N)
								: undefined}
							down={imageData.phoneConfig.descriptionPos !== Directions.S
								? () => (imageData.phoneConfig.descriptionPos = Directions.S)
								: undefined}
							bind:preview
						>
							<div class="max-w-9/10 mx-auto">
								<EditorDescription
									id={imageData.filename}
									bind:descriptionEs={imageData.descriptionEs}
									bind:descriptionEn={imageData.descriptionEn}
									bind:descriptionAlignment={imageData.phoneConfig.descriptionAlignment}
									bind:descriptionFont={imageData.descriptionFont}
									bind:preview
								/>
							</div>
						</Movable>
					{/if}
					<div
						class={`relative transition-all ${[Alignment.Derecha, Alignment.Izquierda].includes(imageData.phoneConfig.alignment) ? 'w-2/3' : ''}`}
						class:ml-auto={imageData.phoneConfig.alignment === Alignment.Derecha}
						class:mr-auto={imageData.phoneConfig.alignment === Alignment.Izquierda}
					>
						<img src={imageData.imageUrl} alt={imageData.altText} class="size-full" />
						<div class="absolute top-0 flex justify-between h-10 w-full">
							<button
								class="hover:bg-gray-700/70 h-full p-2 cursor-pointer"
								onclick={() => {
									if (imageData.phoneConfig.descriptionPos)
										imageData.phoneConfig.descriptionPos = null;
									else
										imageData.phoneConfig.descriptionPos = imageData.phoneConfig.descriptionPos =
											Directions.S;
								}}
							>
								<span class="material-symbols-outlined">
									{imageData.phoneConfig.descriptionPos ? 'close' : 'description'}
								</span>
							</button>
							<div class="bg-gray-400 flex items-center">
								<label for={`alignment-${imageData.filename}`} class="h-full p-2">
									Alineación:
								</label>
								<select
									id={`alignment-${imageData.filename}`}
									bind:value={imageData.phoneConfig.alignment}
								>
									{#each Object.entries(Alignment) as [label, val] (val)}
										<option value={val} class="bg-black">{label}</option>
									{/each}
								</select>
							</div>
						</div>
					</div>
				</div>
			</Borders>
		{:else}
			<div class:px-8={imageData.phoneConfig.alignment !== Alignment.Sangrar}>
				<div
					class={`border-vector-orange my-20 gap-12 flex ${
						imageData.phoneConfig.borders.e && 'border-r-2 pr-30'
					} ${imageData.phoneConfig.borders.w && 'border-l-2 pl-30'} ${
						imageData.phoneConfig.borders.n && 'border-t-2 pt-30'
					} ${imageData.phoneConfig.borders.s && 'border-b-2 pb-30'}`}
					class:justify-center={imageData.phoneConfig.alignment === Alignment.Centro}
					class:flex-row={imageData.phoneConfig.descriptionPos === Directions.W}
					class:flex-row-reverse={imageData.phoneConfig.descriptionPos === Directions.E}
					class:flex-col={imageData.phoneConfig.descriptionPos === Directions.N}
					class:flex-col-reverse={imageData.phoneConfig.descriptionPos === Directions.S}
				>
					{#if imageData.descriptionEs && imageData.phoneConfig.descriptionPos}
						<div
							class={`max-w-9/10 mx-auto markdownDescription font-${imageData.descriptionFont} ${imageData.phoneConfig.descriptionAlignment}`}
						>
							<EditorDescription
								id={imageData.filename}
								bind:descriptionEs={imageData.descriptionEs}
								bind:descriptionEn={imageData.descriptionEn}
								bind:descriptionAlignment={imageData.phoneConfig.descriptionAlignment}
								bind:descriptionFont={imageData.descriptionFont}
								bind:preview
							/>
						</div>
					{/if}
					<div>
						<img
							src={imageData.imageUrl}
							alt={imageData.altText}
							class={`${[Alignment.Derecha, Alignment.Izquierda].includes(imageData.phoneConfig.alignment) ? 'w-2/3' : ''}`}
							class:ml-auto={imageData.phoneConfig.alignment === Alignment.Derecha}
							class:mr-auto={imageData.phoneConfig.alignment === Alignment.Izquierda}
						/>
					</div>
				</div>
			</div>
		{/if}
	</div>
{/snippet}

<div class="bg-black p-5 flex justify-center">
	<div class="fixed top-5 right-5 flex flex-col items-end gap-2 z-30 opacity-70 hover:opacity-100">
		<input id="previewToggle" type="checkbox" bind:checked={preview} hidden />
		<label
			for="previewToggle"
			title="Vista Previa"
			class="hover:cursor-pointer z-10 bg-gray-200/30 hover:bg-gray-200 rounded-xs"
		>
			<span class="material-symbols-outlined text-4xl select-none">
				{preview ? 'preview_off' : 'preview'}
			</span>
		</label>
		<button
			class="bg-green-500 disabled:brightness-50 hover:brightness-90 p-2 disabled:cursor-not-allowed rounded-xs transition-colors"
			disabled={!saveEnabled}
			onclick={updateMobileConfig}>Guardar</button
		>
		<button
			class="bg-red-500 disabled:brightness-50 hover:brightness-90 disabled:cursor-not-allowed p-2 rounded-xs transition-colors"
			disabled={!saveEnabled}
			onclick={() => {
				updatedProjectData = $state.snapshot(originalProjectData);
			}}>Cancelar cambios</button
		>
	</div>
	<Phone>
		<div class="text-white">
			<header class="bg-vector-grey flex h-20 items-center justify-center gap-20 p-3 mb-12">
				<a href="/" class="h-full">
					<img src={logo} alt="logo" class="h-full" />
				</a>
				<p
					class="font-Agency-FB hidden w-fit text-center text-4xl tracking-widest @xl:inline"
					style="word-spacing: 1.5rem;"
				>
					Obras únicas y exclusivas
				</p>
			</header>
			{#each updatedProjectData.spaces.slice(0, 1) as space, i (space.id)}
				{@const firstImage = space.images.find((x: any) => !x.hideInProject)}

				<Movable
					down={() => {
						const fromIndex = 0;
						const image = space.images[fromIndex];
						space.images.splice(fromIndex, 1);
						space.images.splice(fromIndex + 1, 0, image);
					}}
					bind:preview
					class="my-12"
				>
					{@render imageEditor(firstImage)}
				</Movable>
				<div class="px-8 my-12 text-white">
					{#if !preview}
						<div
							class="w-full flex font-Agency-FB border-b-vector-orange my-2 border-b-2 pb-2 text-3xl items-center"
						>
							<input
								type="text"
								bind:value={updatedProjectData.name}
								id="projectName"
								class="indent-1 z-10"
							/>
							<label for="projectName" class="cursor-pointer hover:bg-gray-700 p-1 rounded-md"
								><span class="material-symbols-outlined"> edit </span></label
							>
						</div>
					{:else}
						<h1
							class="font-Agency-FB border-b-vector-orange my-2 border-b-2 pb-2 indent-1 text-3xl w-full"
						>
							{updatedProjectData.name}
						</h1>
					{/if}
					{#if !preview}
						<p class="font-Arial text-right text-sm">
							Área: <input
								type="number"
								bind:value={updatedProjectData.area}
								class="w-18 appearance-none border-dashed border-2 border-white p-1"
							/> metros cuadrados
						</p>
					{:else}
						<p class="font-Arial text-right text-sm">
							Área: {updatedProjectData.area} metros cuadrados
						</p>
					{/if}
					<div class="my-6">
						<EditorDescription
							id={updatedProjectData.id}
							bind:descriptionEs={updatedProjectData.descriptionEs}
							bind:descriptionEn={updatedProjectData.descriptionEn}
							descriptionAlignment="text-justify"
							bind:preview
						/>
					</div>
				</div>

				{#each space.images as image, i (image.filename)}
					{#if image !== firstImage && !image.hideInProject}
						<Movable
							up={i > 0
								? () => {
										const fromIndex = i;
										const image = space.images[i];
										space.images.splice(fromIndex, 1);
										space.images.splice(fromIndex - 1, 0, image);
									}
								: undefined}
							down={i < space.images.length - 1
								? () => {
										const fromIndex = i;
										const image = space.images[i];
										space.images.splice(fromIndex, 1);
										space.images.splice(fromIndex + 1, 0, image);
									}
								: undefined}
							bind:preview
							class="my-12"
						>
							{@render imageEditor(image)}
						</Movable>
					{/if}
				{/each}
				{#if !preview}
					<hr class="h-2 border-dashed border-green-600" />
				{/if}
			{/each}
			{#each updatedProjectData.spaces.slice(1) as space, i (space.id)}
				{#each space.images as image, i (image.filename)}
					{#if !image.hideInProject}
						<Movable
							up={i > 0 ? () => {} : undefined}
							down={i < space.images.length - 1 ? () => {} : undefined}
							bind:preview
							class="my-12"
						>
							{@render imageEditor(image)}
						</Movable>
					{/if}
				{/each}
				{#if !preview}
					<hr class="h-2 border-dashed border-green-600" />
				{/if}
			{/each}
		</div>
	</Phone>
</div>
