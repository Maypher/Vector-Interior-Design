<script lang="ts">
	interface Props {
		onclick: () => void;
		children: any;
	}

	const { onclick, children }: Props = $props();
</script>

<button type="button" class="hover:bg-black hover:text-white rounded-md text-sm size-6" {onclick}
	>{@render children()}
</button>
