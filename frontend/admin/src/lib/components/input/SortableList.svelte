<script lang="ts">
	import Sortable, { type Options } from 'sortablejs';
	import { onMount, type Snippet } from 'svelte';

	let {
		sortable = $bindable(),
		sortableOptions,
		sortableId,
		children
	}: {
		sortable?: Sortable;
		sortableOptions?: Options;
		sortableId: string;
		children: Snippet<[]>;
	} = $props();

	onMount(() => {
		const element = document.getElementById(sortableId) as HTMLElement;
		sortable = Sortable.create(element, sortableOptions);
	});
</script>

{@render children()}
