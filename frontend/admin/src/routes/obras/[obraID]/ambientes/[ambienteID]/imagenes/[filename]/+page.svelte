<script lang="ts">
	import { yup } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { superForm } from 'sveltekit-superforms';
	import { imageUpdateSchema } from '$lib/utilities/yupSchemas';
	import EditableInput from '$lib/components/input/EditableInput.svelte';
	import { PUBLIC_apiUrl } from '$env/static/public';
	import { success } from '$lib/utilities/toasts';
	import confirmationDialog from '$lib/utilities/dialog';
	import { goto } from '$app/navigation';
	import graphql from '$lib/utilities/api';

	const { data }: { data: PageData } = $props();
	let imageData = $state(data.imageData!);
	let submitting: boolean = $state(false);
	let deleteDialog: HTMLDialogElement | null | undefined = $state();

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
				deleteImage(filename: $filename) {
					filename
				}
			}
		`;

			const variables = { filename: imageData.filename };

			await graphql(query, variables);

			await goto(`/obras/${data.obraId}/ambientes/${data.ambienteId}`);
		}
	}
</script>

<div class="w-full bg-green-600">
	<button onclick={deleteImage}>Borrar Imagen</button>
	<img src={`http://localhost:8080/images/${imageData.filename}`} alt={imageData.altText} />

	<form use:enhance>
		<fieldset disabled={submitting}>
			<EditableInput
				name="name"
				label="Nombre"
				bind:value={$form.altText}
				errors={$errors.altText}
				type="text"
				{...$constraints.altText}
			/>
			<button>Actualizar</button>
		</fieldset>
	</form>
</div>
