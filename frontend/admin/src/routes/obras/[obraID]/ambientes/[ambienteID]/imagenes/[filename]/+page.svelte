<script lang="ts">
	import { yup } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { superForm } from 'sveltekit-superforms';
	import { imageUpdateSchema } from '$lib/utilities/yupSchemas';
	import { success } from '$lib/utilities/toasts';
	import confirmationDialog from '$lib/utilities/dialog';
	import { goto } from '$app/navigation';
	import graphql from '$lib/utilities/api';

	const { data }: { data: PageData } = $props();
	let imageData = $state(data.imageData!);
	let isThumbnail = $derived(imageData.space.project.thumbnail?.filename === imageData.filename);
	let isInMainPage = $derived(imageData.mainPage);
	let submitting: boolean = $state(false);
	let english: boolean = $state(false);

	const { form, errors, enhance, constraints } = superForm(data.updateForm!, {
		SPA: true,
		validators: yup(imageUpdateSchema),
		resetForm: false,
		async onUpdate({ form: updateForm }) {
			submitting = true;
			if (updateForm.valid) {
				const query = `
					mutation updateImage($filename: String!, $altTextEs: String, $altTextEn: String, $descriptionEs: String, 
					$descriptionEn: String, $descriptionFont: String, $hideInProject: Boolean, $sculpture: Boolean) {
						updateImage(filename: $filename, altTextEs: $altTextEs, altTextEn: $altTextEn, descriptionEs: $descriptionEs, 
						descriptionEn: $descriptionEn, descriptionFont: $descriptionFont, hideInProject: $hideInProject, sculpture: $sculpture) {
							altTextEs
							altTextEn
							descriptionEs
							descriptionEn
							descriptionFont
							hideInProject
							sculpture
						}
					}
				`;

				const variables = { filename: imageData.filename, ...updateForm.data };

				const updatedImageData = (await graphql(query, variables)).updateImage;
				success(`Imagen actualizada con éxito.`);
				$form.altTextEs = updatedImageData.altTextEs;
				$form.altTextEn = updatedImageData.altTextEn;
				$form.descriptionEs = updatedImageData.descriptionEs;
				$form.descriptionEn = updatedImageData.descriptionEn;
				$form.descriptionFont = updatedImageData.descriptionFont;
				$form.hideInProject = updatedImageData.hideInProject;
				$form.sculpture = updatedImageData.sculpture;
			}
			submitting = false;
		}
	});

	let phoneConfig = $state($state.snapshot(imageData.phoneConfig));

	async function deleteImage() {
		if (
			await confirmationDialog(
				'Seguro que deseas eliminar esta imagen? Esta acción no puede ser revertida.'
			)
		) {
			const query = `
				mutation deleteImage($filename: String!) {
					deleteImage(filename: $filename)
				}
			`;

			const variables = { filename: imageData.filename };

			const deleted = (await graphql(query, variables)).deleteImage;

			if (deleted) await goto(`/obras/${data.projectId}`);
		}
	}

	async function setThumbnail() {
		const query = `
			mutation setThumbnail($projectId: Int!, $thumbnail: Int) {
				updateProject(id: $projectId, thumbnail: $thumbnail) {
					name
					thumbnail {
						id
						filename
					}
				}
			}
		`;

		const variables = {
			projectId: data.projectId,
			thumbnail: isThumbnail ? null : imageData.id
		};

		const projectData = (await graphql(query, variables)).updateProject;

		imageData.space.project.thumbnail = projectData.thumbnail;

		success(
			isThumbnail
				? `Imagen colocada como imagen principal de "${projectData.name}"`
				: `Imagen removida como imagen principal de ${projectData.name}`
		);
	}

	async function setMainPage() {
		const query = `
			mutation setMainPage($filename: String!, $mainPage: Boolean) {
				updateImage(filename: $filename, mainPage: $mainPage) {
					mainPage
				}
			}
		`;

		const variables = { filename: imageData.filename, mainPage: !imageData.mainPage };

		const imageDataUpdated = (await graphql(query, variables)).updateImage;

		imageData.mainPage = imageDataUpdated.mainPage;

		success(
			isInMainPage
				? 'Imagen colocada en la página principal.'
				: 'Imagen removida de la página principal'
		);
	}
</script>

<div class="w-full lg:h-[calc(100svh-5rem)] bg-black lg:p-3">
	<form
		use:enhance
		class="m-auto flex flex-col lg:flex-row w-fit h-full gap-x-20 bg-zinc-500 p-3 lg:rounded-md"
	>
		<div class="flex flex-col justify-between h-full">
			<h1 class="text-xl text-center">
				Imagen de <b>{imageData.space.name}</b> en
				<a href={`/obras/${imageData.space.project.id}`} class="border-b-2 border-black"
					>{imageData.space.project.name}</a
				>
			</h1>
			<img
				src={imageData.imageUrl}
				alt={imageData.altTextEs}
				class="h-full w-auto my-2 shadow-md shadow-black"
			/>
			<div class="flex justify-around items-center text-4xl">
				<button
					onclick={setThumbnail}
					type="button"
					class="w-fit p-2 text-yellow-300 hover:text-yellow-200 transition-colors cursor-pointer"
					title={isThumbnail ? 'Imagen principal' : 'Colocar como imagen principal'}
				>
					{isThumbnail ? '★' : '☆'}
				</button>
				<button
					onclick={setMainPage}
					type="button"
					class={`w-fit p-2 ${isInMainPage ? 'text-yellow-300' : 'text-black'} cursor-pointer`}
					title={isInMainPage ? 'Remover de página principal' : 'Colocar en página principal'}
				>
					⌂
				</button>
				<button
					onclick={deleteImage}
					type="button"
					class="w-fit p-2 text-red-500 hover:text-black transition-colors cursor-pointer"
					>x
				</button>
			</div>
		</div>
		<fieldset disabled={submitting} class="flex flex-col justify-evenly">
			<div class="flex flex-col gap-2">
				<div>
					<label for="alt-text">Texto Alternativo</label>
					<label class="bg-vector-orange border-2 border-black p-1" for="alt-text-lang"
						>{english ? 'Ingles' : 'Español'}</label
					>
					<input type="checkbox" id="alt-text-lang" bind:checked={english} hidden />
				</div>
				{#if english}
					<input type="text" bind:value={$form.altTextEn} class="p-2 bg-white rounded-md" />
				{:else}
					<input type="text" bind:value={$form.altTextEs} class="p-2 bg-white rounded-md" />
				{/if}
			</div>
			<div class="flex flex-col gap-2">
				<div>
					<label for="description">Descripción</label>
					<label class="bg-vector-orange border-2 border-black p-1" for="desc-lang"
						>{english ? 'Ingles' : 'Español'}</label
					>
					<input type="checkbox" id="desc-lang" bind:checked={english} hidden />
				</div>
				{#if english}
					<textarea
						id="description"
						class={`min-h-40 max-h-50 font-${$form.descriptionFont} border-2 border-dashed border-white p-2 bg-gray-600 text-white`}
						bind:value={$form.descriptionEn}
					></textarea>
				{:else}
					<textarea
						id="description"
						class={`min-h-40 max-h-50 font-${$form.descriptionFont} border-2 border-dashed border-white p-2 bg-gray-600 text-white`}
						bind:value={$form.descriptionEs}
					></textarea>
				{/if}
			</div>

			<div class="my-2">
				<label for="descriptionFont">Tipografía de Descripción</label>
				<select id="descriptionFont" bind:value={$form.descriptionFont} class="bg-white">
					<option value="Arial" class="font-Arial">Arial</option>
					<option value="Agency-FB" class="font-Agency-FB">Agency-FB</option>
					<option value="Bahnschrift" class="font-Bahnschrift">Bahnschrift</option>
				</select>
			</div>
			<div>
				<label for="hideInProject">Esconder en proyecto</label>
				<input id="hideInProject" type="checkbox" bind:checked={$form.hideInProject} />
			</div>
			<div>
				<label for="sculpture">Escultura</label>
				<input id="sculpture" type="checkbox" bind:checked={$form.sculpture} />
			</div>
			<button
				class="bg-green-500 p-2 rounded-md hover:bg-orange-800 my-5 self-start transition-colors cursor-pointer"
				>Actualizar
			</button>
		</fieldset>
	</form>
</div>
