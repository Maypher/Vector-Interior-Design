<script lang="ts">
	interface Props {
		imageId: string;
		color: string;
	}

	const baseColors = [
		{
			hex: '#101214',
			label: 'Negro'
		},
		{
			hex: '#1c2025',
			label: 'Gris'
		}
	];

	let { imageId, color = $bindable() }: Props = $props();
	let customColor: boolean = $state(!baseColors.some((x) => x.hex === color));
</script>

<div class="p-2 rounded-sm">
	<div>
		<label for={`${imageId}-bgColor`} class="font-bold">Color de fondo</label>
		<span>
			<label
				for={`${imageId}-custom`}
				class={`transition-colors cursor-pointer ${customColor ? 'bg-vector-cream/50' : ''}`}
			>
				&#127912;
			</label>
			<input id={`${imageId}-custom`} type="checkbox" bind:checked={customColor} hidden />
		</span>
	</div>
	{#if !customColor}
		<select id={`${imageId}-bgColor`} bind:value={color} class="bg-vector-cream text-black">
			{#each baseColors as baseColor}
				<option value={baseColor.hex} selected={baseColor.hex === color}>{baseColor.label}</option>
			{/each}
		</select>
	{:else}
		<input id={`${imageId}-bgColor`} type="color" bind:value={color} />
	{/if}
</div>
