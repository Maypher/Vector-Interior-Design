<script lang="ts">
	interface Props {
		saveEnabled: boolean;
		preview: boolean;
		onSaveClick: () => void;
		onCancelClick: () => void;
	}

	let { saveEnabled, preview = $bindable(false), onSaveClick, onCancelClick }: Props = $props();
</script>

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
		onclick={onSaveClick}>Guardar</button
	>
	<button
		class="bg-red-500 disabled:brightness-50 hover:brightness-90 disabled:cursor-not-allowed p-2 rounded-xs transition-colors"
		disabled={!saveEnabled}
		onclick={onCancelClick}>Cancelar cambios</button
	>
</div>
