<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		id: string;
		n?: boolean;
		s?: boolean;
		e?: boolean;
		w?: boolean;
		preview?: boolean;
		children: Snippet;
		[key: string]: any;
	}

	let {
		id,
		n = $bindable(undefined),
		s = $bindable(undefined),
		e = $bindable(undefined),
		w = $bindable(undefined),
		preview = $bindable(false),
		children,
		...props
	}: Props = $props();
</script>

<div {...props} class={`relative ${props.class}`}>
	{#if !preview && n !== undefined}
		<input type="checkbox" id={`logo-border-n-${id}`} hidden bind:checked={n} />
		<label
			for={`logo-border-n-${id}`}
			class={`w-full h-2 absolute -top-5 left-0 hover:cursor-pointer hover:bg-vector-orange/40 ${n ? 'bg-vector-orange' : 'bg-gray-600/40'}`}
		></label>
	{/if}
	{#if !preview && w !== undefined}
		<input type="checkbox" id={`logo-border-w-${id}`} hidden bind:checked={w} />
		<label
			for={`logo-border-w-${id}`}
			class={`w-2 h-full absolute -left-5 hover:cursor-pointer hover:bg-vector-orange/40 ${w ? 'bg-vector-orange' : 'bg-gray-600/40'}`}
		></label>
	{/if}
	{@render children()}
	{#if !preview && s !== undefined}
		<input type="checkbox" id={`logo-border-s-${id}`} hidden bind:checked={s} />
		<label
			for={`logo-border-s-${id}`}
			class={`w-full h-2 absolute left-0 -bottom-5 hover:cursor-pointer hover:bg-vector-orange/40 ${s ? 'bg-vector-orange' : 'bg-gray-600/40'}`}
		></label>
	{/if}
	{#if !preview && e !== undefined}
		<input type="checkbox" id={`logo-border-e-${id}`} hidden bind:checked={e} />
		<label
			for={`logo-border-e-${id}`}
			class={`w-2 h-full absolute -right-5 top-0 hover:cursor-pointer hover:bg-vector-orange/40 ${e ? 'bg-vector-orange' : 'bg-gray-600/40'}`}
		></label>
	{/if}
</div>
