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

	const { data }: { data: PageData } = $props();
	let imageData = $state(data.imageData!);
	let submitting: boolean = $state(false);

	const { form, errors, enhance, constraints } = superForm(data.updateForm!, {
		SPA: true,
		validators: yup(imageUpdateSchema),
		resetForm: false,
		async onUpdate({ form: updateForm }) {
			submitting = true;
			if (updateForm.valid) {
				const query = `
					mutation updateImage($filename: String!, $altText: String!) {
						updateImage(filename: $filename, altText: $altText) {
							altText
						}
					}
				`;

				const variables = { filename: imageData.filename, ...updateForm.data };

				const updatedImageData = (await graphql(query, variables)).updateImage;
				success(`Imagen actualizada con éxito.`);
				$form.altText = updatedImageData.altText;
			}
			submitting = false;
		}
	});

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
			mutation setThumbnail($obraId: Int!, $thumbnail: String!) {
				updateObra(id: $obraId, thumbnail: $thumbnail) {
					name
				}
			}
		`;

		const variables = { obraId: data.obraId, thumbnail: imageData.filename };

		const obraName = (await graphql(query, variables)).updateObra.name;

		success(`Imagen colocada como imagen principal de "${obraName}"`);
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
			class="block w-fit ml-auto m-1 p-2 bg-green-500 hover:bg-blue-700"
		>
			Colocar como imagen principal
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
			<button class="bg-green-500 p-2 rounded-md hover:bg-orange-800">Actualizar</button>
		</fieldset>
	</form>
</div>
