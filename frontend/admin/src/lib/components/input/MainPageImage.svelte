<script lang="ts">
	import { PUBLIC_imageURL } from '$env/static/public';
	import { Directions } from '$lib/utilities/enums';
	import Markdown from '../markdown/Markdown.svelte';
	import graphql from '$lib/utilities/api';
	import { success } from '$lib/utilities/toasts';

	interface ImageConfig {
		id: number;
		description: string | undefined;
		descriptionEn: string | undefined;
		descriptionPos: string | null;
		descriptionFontSize: number;
		descriptionFont: string;
		descriptionAlignment: string;
		logoPos: string | null;
		overflow: boolean;
		logoBorders: {
			n: boolean;
			s: boolean;
			e: boolean;
			o: boolean;
		};
		imageBorders: {
			n: boolean;
			s: boolean;
			e: boolean;
			o: boolean;
		};
	}

	interface Props {
		image: {
			filename: string;
			altText: string;
			ambienteId: number;
			obraId: number;
		};
		imageConfig: ImageConfig;
	}

	const { image, imageConfig }: Props = $props();

	// Done this way because prop passed by reference and when updating it updates the value in the parent.
	// This forces a deep copy so it is treated as a different value.
	let configClone = $state.snapshot(imageConfig);
	let originalConfig: ImageConfig = $state(configClone);
	let updatedConfig: ImageConfig = $state(configClone);
	let shouldUpdate: boolean = $derived(
		JSON.stringify(originalConfig) !== JSON.stringify(updatedConfig)
	);

	let showDescriptions: boolean = $state(false);
	let descriptionEn: boolean = $state(false);

	async function onsubmit(evt: SubmitEvent) {
		evt.preventDefault();

		console.log($state.snapshot(updatedConfig));

		const query = `
			mutation updateImageConfig($id: Int!, $description: String, $descriptionEn: String, 
			$logoPos: Direction, $descriptionPos: Direction, $descriptionAlignment: String, 
			$descriptionFont: String, $descriptionFontSize: Float,
			$overflow: Boolean, $imageBorders: BordersInput, 
			$logoBorders: BordersInput) {
				updateImageConfig(id: $id, description: $description, descriptionEn: $descriptionEn,
				logoPos: $logoPos, descriptionPos: $descriptionPos,
				descriptionAlignment: $descriptionAlignment, descriptionFont: $descriptionFont, 
				descriptionFontSize: $descriptionFontSize, overflow: $overflow, 
				imageBorders: $imageBorders, logoBorders: $logoBorders) {
					id
					description
					descriptionEn
					logoPos
					descriptionPos
					descriptionAlignment
					descriptionFont
					descriptionFontSize
					overflow
					imageBorders {
						n
						s
						e
						o
					}
					logoBorders {
						n
						s
						e
						o
					}
				}
			}
		`;

		const updates = $state.snapshot(updatedConfig);

		const updatedData = (await graphql(query, updates)).updateImageConfig;

		console.log(updatedData);
		originalConfig = updatedData;
		updatedConfig = updatedData;

		success('Información actualizada correctamente.');
	}
</script>

<form {onsubmit} class="flex justify-between pl-2 w-full">
	<div class="flex flex-col gap-2 accent-[#ff4800] m-2">
		<input type="checkbox" bind:checked={updatedConfig.imageBorders.n} />
		<div class="flex gap-2">
			<input type="checkbox" bind:checked={updatedConfig.imageBorders.o} />
			<a href={`/obras/${image.obraId}/ambientes/${image.ambienteId}/imagenes/${image.filename}`}>
				<img src={`${PUBLIC_imageURL}${image.filename}`} alt={image.altText} class="h-36" />
			</a>
			<input type="checkbox" bind:checked={updatedConfig.imageBorders.e} />
		</div>
		<input type="checkbox" bind:checked={updatedConfig.imageBorders.s} />
	</div>
	<div>
		<div class="flex gap-5 p-5 items-center">
			<div>
				<label for={`overflow-${imageConfig.id}`}>Sangrar</label>
				<input
					type="checkbox"
					name="overflow"
					id={`overflow-${imageConfig.id}`}
					bind:checked={updatedConfig.overflow}
				/>
			</div>
			<div class="flex flex-col gap-2">
				<input
					type="checkbox"
					bind:checked={updatedConfig.logoBorders.n}
					class="accent-[#ff4800]"
				/>
				<div class="flex gap-2">
					<input
						type="checkbox"
						bind:checked={updatedConfig.logoBorders.o}
						class="accent-[#ff4800]"
					/>
					<div class="flex flex-col">
						<label for="logoPos" class="m-auto">Logo</label>
						<select name="logoPos" bind:value={updatedConfig.logoPos}>
							{#each Object.entries(Directions) as [direction, value] (direction)}
								<option {value} selected={value === imageConfig.logoPos}>{direction}</option>
							{/each}
						</select>
					</div>
					<input
						type="checkbox"
						bind:checked={updatedConfig.logoBorders.e}
						class="accent-[#ff4800]"
					/>
				</div>
				<input
					type="checkbox"
					bind:checked={updatedConfig.logoBorders.s}
					class="accent-[#ff4800]"
				/>
			</div>
			<div class="flex flex-col items-center gap-2">
				<div>
					<label for="textPos">Posición de Descripción</label>
					<select name="textPos" bind:value={updatedConfig.descriptionPos}>
						{#each Object.entries(Directions) as [direction, value] (direction)}
							<option {value} selected={value === imageConfig.descriptionPos}>{direction} </option>
						{/each}
					</select>
				</div>
				<div>
					<label for={`descriptionFont-${imageConfig.id}`}>Tipografía de descripción</label>
					<select
						name="descriptionFont"
						id={`descriptionFont-${imageConfig.id}`}
						bind:value={updatedConfig.descriptionFont}
					>
						<option value="Arial" class="font-[Arial]">Arial</option>
						<option value="Agency-FB" class="font-[Agency-FB]">Agency-FB</option>
						<option value="Bahnschrift" class="font-[Agency-FB]">Bahnschrift</option>
					</select>
				</div>
				<div>
					<label for={`descriptionAlignment-${imageConfig.id}`}>Alineación de descripción</label>
					<select
						name="descriptionAlignment"
						id={`descriptionAlignment-${imageConfig.id}`}
						bind:value={updatedConfig.descriptionAlignment}
					>
						<option value="text-center">Centrar</option>
						<option value="text-justify">Justificar</option>
						<option value="text-left">Izquierda</option>
						<option value="text-right">Derecha</option>
					</select>
				</div>
				<div class="flex items-center">
					<label for={`descriptionFontSize-${imageConfig.id}`}>Tamaño de descripción</label>
					<input
						type="range"
						min="0.5"
						max="8"
						step="0.1"
						name="fontSize"
						bind:value={updatedConfig.descriptionFontSize}
					/>
					<input
						type="number"
						step="0.1"
						name="fontSize"
						bind:value={updatedConfig.descriptionFontSize}
						class="w-10"
					/>
				</div>
			</div>
		</div>
		<div>
			<div class="w-full bg-green-300 flex items-center p-2">
				<label for={`showDescription-${imageConfig.id}`} class="w-full select-none"
					>Descripciones</label
				>
				<input
					type="checkbox"
					id={`showDescription-${imageConfig.id}`}
					form={null}
					bind:checked={showDescriptions}
					class="hidden"
				/>
				<span
					class="material-symbols-outlined transition-transform"
					class:rotate-180={showDescriptions}
				>
					keyboard_arrow_up
				</span>
			</div>
			<div
				class="transition-all overflow-hidden"
				class:max-h-0={!showDescriptions}
				class:max-h-screen={showDescriptions}
			>
				<div class="flex w-full">
					<button
						type="button"
						class="bg-red-200 w-full hover:bg-red-500"
						class:bg-red-500={!descriptionEn}
						onclick={() => (descriptionEn = false)}>Español</button
					>
					<button
						type="button"
						class="bg-red-200 w-full hover:bg-red-500"
						class:bg-red-500={descriptionEn}
						onclick={() => (descriptionEn = true)}>Ingles</button
					>
				</div>
				<div class:hidden={!descriptionEn}>
					<Markdown
						label="Descripción (Ingles)"
						name="descriptionEn"
						bind:value={updatedConfig.descriptionEn}
						errors={[]}
					/>
				</div>
				<div class:hidden={descriptionEn}>
					<Markdown
						label="Descripción"
						name="description"
						bind:value={updatedConfig.description}
						errors={[]}
					/>
				</div>
			</div>
		</div>
	</div>
	<div
		class="flex flex-col justify-center gap-2 overflow-hidden transition-all ease-out duration-500"
		class:max-w-0={!shouldUpdate}
		class:p-2={shouldUpdate}
	>
		<button
			type="submit"
			class="text-green-600 hover:bg-green-600 hover:text-white rounded-md transition-all"
			title="Guardar cambios"
			><span class="material-symbols-outlined h-full content-center"> check </span></button
		>
		<button
			type="button"
			class="text-red-600 hover:bg-red-600 hover:text-white rounded-md transition-all"
			title="Revertir cambios"
			onclick={() => (updatedConfig = configClone)}
			><span class="material-symbols-outlined h-full content-center"> cancel </span></button
		>
	</div>
</form>

<style>
	@font-face {
		font-family: 'Agency-FB';
		font-style: normal;
		font-weight: 400;
		src: url('/fonts/agency-fb.ttf');
	}

	@font-face {
		font-family: 'Bahnschrift';
		font-style: normal;
		font-weight: 100;
		src: url('/fonts/bahnschrift.ttf');
	}
</style>
