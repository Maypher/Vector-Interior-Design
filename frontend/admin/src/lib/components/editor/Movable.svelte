<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		up?: () => void;
		down?: () => void;
		left?: () => void;
		right?: () => void;
		children: Snippet;
		preview?: boolean;
		[key: string]: unknown;
	}

	const { up, down, left, right, children, preview = $bindable(false), ...props }: Props = $props();
</script>

<div
	{...props}
	class={`relative ${!preview ? 'border-dashed border-2 border-gray-500' : ''} ${props.class}`}
>
	{#if !preview && up}
		<button
			class="absolute -top-7 left-1/2 z-10 -translate-x-1/2 w-full max-w-24 backdrop-blur-xs flex justify-center items-center rounded-t-md hover:bg-gray-600/30 transition-colors"
			onclick={up}
		>
			<span class="material-symbols-outlined content-center text-white"> keyboard_arrow_up </span>
		</button>
	{/if}
	{#if !preview && down}
		<button
			class="absolute -bottom-7 left-1/2 z-10 -translate-x-1/2 w-full max-w-24 backdrop-blur-xs flex justify-center items-center rounded-d-md hover:bg-gray-600/30 transition-colors"
			onclick={down}
		>
			<span class="material-symbols-outlined content-center text-white">keyboard_arrow_down</span>
		</button>
	{/if}
	{#if !preview && left}
		<button
			class="absolute top-1/2 z-10 h-full flex items-center justify-center max-h-24 -left-7 backdrop-blur-xs rounded-l-md -translate-y-1/2 hover:bg-gray-200/30 transition-colors"
			onclick={left}
		>
			<span class="material-symbols-outlined text-white h-full content-center">
				keyboard_arrow_left
			</span>
		</button>
	{/if}
	{#if !preview && right}
		<button
			class="absolute top-1/2 z-10 h-full max-h-24 -right-7 backdrop-blur-xs rounded-r-md -translate-y-1/2 hover:bg-gray-200/30 transition-colors"
			onclick={right}
		>
			<span class="material-symbols-outlined text-white h-full content-center">
				keyboard_arrow_right
			</span>
		</button>
	{/if}
	{@render children()}
</div>
