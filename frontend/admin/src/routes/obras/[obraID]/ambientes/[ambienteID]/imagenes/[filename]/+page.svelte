<script lang="ts">
	import { yup } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { superForm } from 'sveltekit-superforms';
	import { imageUpdateSchema } from '$lib/utilities/yupSchemas';
	import EditableInput from '$lib/components/input/EditableInput.svelte';
	import { success } from '$lib/utilities/toasts';
	import confirmationDialog from '$lib/utilities/dialog';
	import { goto } from '$app/navigation';
	import graphql from '$lib/utilities/api';
	import { PUBLIC_imageURL } from '$env/static/public';
	import Markdown from '$lib/components/markdown/Markdown.svelte';
	import { Alignment, Directions } from '$lib/utilities/enums';

	const { data }: { data: PageData } = $props();
	let imageData = $state(data.imageData!);
	let isThumbnail = $derived(imageData.ambiente.obra.thumbnail?.filename === imageData.filename);
	let isInMainPage = $derived(imageData.mainPage);
	let submitting: boolean = $state(false);

	const { form, errors, enhance, constraints } = superForm(data.updateForm!, {
		SPA: true,
		validators: yup(imageUpdateSchema),
		resetForm: false,
		async onUpdate({ form: updateForm }) {
			submitting = true;
			if (updateForm.valid) {
				const query = `
					mutation updateImage($filename: String!, $altText: String!, $description: String, $descriptionFont: String, $hideInProject: Boolean) {
						updateImage(filename: $filename, altText: $altText, description: $description, descriptionFont: $descriptionFont, hideInProject: $hideInProject) {
							altText
							description
							descriptionFont
							hideInProject
						}
					}
				`;

				const variables = { filename: imageData.filename, ...updateForm.data };

				const updatedImageData = (await graphql(query, variables)).updateImage;
				success(`Imagen actualizada con éxito.`);
				$form.altText = updatedImageData.altText;
				$form.description = updatedImageData.description;
				$form.descriptionFont = updatedImageData.descriptionFont;
				$form.hideInProject = updatedImageData.hideInProject;
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

			await goto(`/obras/${data.obraId}/ambientes/${data.ambienteId}`);
		}
	}

	async function setThumbnail() {
		const query = `
			mutation setThumbnail($obraId: Int!, $thumbnail: String) {
				updateObra(id: $obraId, thumbnail: $thumbnail) {
					name
					thumbnail {
						filename
					}
				}
			}
		`;

		const variables = { obraId: data.obraId, thumbnail: isThumbnail ? null : imageData.filename };

		const obraData = (await graphql(query, variables)).updateObra;

		imageData.ambiente.obra.thumbnail = obraData.thumbnail;

		success(
			isThumbnail
				? `Imagen colocada como imagen principal de "${obraData.name}"`
				: `Imagen removida como imagen principal de ${obraData.name}`
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

		const obraData = (await graphql(query, variables)).updateImage;

		imageData.mainPage = obraData.mainPage;

		success(
			isInMainPage
				? 'Imagen colocada en la página principal.'
				: 'Imagen removida de la página principal'
		);
	}

	async function updatePhoneConfig(event: SubmitEvent) {
		event.preventDefault();

		const query = `
			mutation updatePhoneConfig($filename: String!, $phoneConfig: phoneConfigInput) {
				updateImage(filename: $filename, phoneConfig: $phoneConfig) {
					phoneConfig {
						borders {
							n
							e
							s
							o
						}
						alignment
						descriptionPos
						descriptionAlignment
					}
				}
			}
		`;

		const updatedConfig = (
			await graphql(query, {
				filename: imageData.filename,
				phoneConfig
			})
		).updateImage.phoneConfig;

		phoneConfig = updatedConfig;

		success('Configuración de teléfono actualizada.');
	}
</script>

<div class="w-full bg-green-600 p-3">
	<form use:enhance class="max-w-xl m-auto bg-zinc-600 p-3 rounded-md">
		<button
			onclick={deleteImage}
			type="button"
			class="block w-fit ml-auto m-1 p-2 bg-red-500 hover:bg-blue-700">Borrar Imagen</button
		>
		<button
			onclick={setThumbnail}
			type="button"
			class={`block w-fit ml-auto m-1 p-2 ${isThumbnail ? 'bg-red-500' : 'bg-green-500'} hover:bg-blue-700`}
		>
			{isThumbnail ? 'Quitar como imagen principal' : 'Colocar como imagen principal'}
		</button>
		<button
			onclick={setMainPage}
			type="button"
			class={`block w-fit ml-auto m-1 p-2 ${isInMainPage ? 'bg-red-500' : 'bg-gray-500'} hover:bg-gray-200`}
		>
			{isInMainPage ? 'Remover de la página principal' : 'Colocar en página principal'}
		</button>
		<img src={`${PUBLIC_imageURL}${imageData.filename}`} alt={imageData.altText} />
		<fieldset disabled={submitting}>
			<EditableInput
				name="altText"
				label="Texto Alternativo"
				bind:value={$form.altText}
				errors={$errors.altText}
				type="text"
				{...$constraints.altText}
			/>
			<Markdown
				label="Descripción"
				name="description"
				bind:value={$form.description}
				errors={$errors.description}
			/>

			<div class="my-2">
				<label for="descriptionFont">Tipografía de Descripción</label>
				<select id="descriptionFont" bind:value={$form.descriptionFont}>
					<option value="Arial" class="font-Arial">Arial</option>
					<option value="Agency-FB" class="font-Agency-FB">Agency-FB</option>
					<option value="Bahnschrift" class="font-Bahnschrift">Bahnschrift</option>
				</select>
			</div>
			<div>
				<label for="hideInProject">Esconder en proyecto</label>
				<input id="hideInProject" type="checkbox" bind:checked={$form.hideInProject} />
			</div>
			<button class="bg-green-500 p-2 rounded-md hover:bg-orange-800 my-5">Actualizar</button>
		</fieldset>
	</form>
	<hr class="my-3" />
	<h1 class="text-xl text-center">Configuración de Teléfono</h1>
	<form onsubmit={updatePhoneConfig} class="bg-blue-500 p-2 max-w-lg m-auto my-10">
		<div class="flex gap-4 items-center">
			<div class="accent-vector-orange flex items-center gap-2">
				<input type="checkbox" bind:checked={phoneConfig.borders.o} />
				<div class="flex flex-col justify-center items-center gap-2">
					<input type="checkbox" bind:checked={phoneConfig.borders.n} />
					<p>Bordes</p>
					<input type="checkbox" bind:checked={phoneConfig.borders.s} />
				</div>
				<input type="checkbox" bind:checked={phoneConfig.borders.e} />
			</div>
			<div>
				<label for="phoneAlignment">Alineación</label>
				<select id="phoneAlignment" bind:value={phoneConfig.alignment}>
					{#each Object.entries(Alignment) as [alignment, value] (alignment)}
						<option {value}>{alignment}</option>
					{/each}
				</select>
			</div>
			<div>
				<div>
					<label for="descriptionPosition">Posición de Descripción</label>
					<select id="descriptionPosition" bind:value={phoneConfig.descriptionPos}>
						{#each Object.entries(Directions) as [alignment, value] (alignment)}
							<option {value}>{alignment}</option>
						{/each}
					</select>
				</div>
				<div>
					<label for="descriptionAlignment">Alineación de la Descripción</label>
					<select id="descriptionAlignment" bind:value={phoneConfig.descriptionAlignment}>
						<option value="text-justify">Justificar</option>
						<option value="text-center">Centrar</option>
						<option value="text-left">Izquierda</option>
						<option value="text-right">Derecha</option>
					</select>
				</div>
			</div>
		</div>
		<div class="mx-auto size-fit">
			<button type="submit" class="my-5 bg-violet-700 p-2 rounded-md hover:bg-violet-500"
				>Actualizar</button
			>
		</div>
	</form>
</div>
