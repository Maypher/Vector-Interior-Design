<script lang="ts">
	import Errors from './Errors.svelte';

	interface Props {
		label: string;
		name: string;
		value?: string;
		errors: Array<string> | undefined;
	}

	let { label, name, value = $bindable(''), errors, ...constrains }: Props = $props();

	let visible = $state(false);
</script>

<div class="my-2 flex flex-col">
	<label for={name} class="block mx-2 my-1">{label}</label>
	<div class="flex align-middle max-w-full bg-white p-1 rounded-md">
		<input
			type={visible ? 'text' : 'password'}
			{name}
			bind:value
			class="focus:outline-hidden"
			{...constrains}
		/>
		<button
			class="material-symbols-outlined size-min m-auto pl-2 border-l-2"
			onclick={() => (visible = !visible)}
			type="button"
		>
			{visible ? 'visibility' : 'visibility_off'}
		</button>
	</div>
	{#if errors}<Errors {errors} />{/if}
</div>
