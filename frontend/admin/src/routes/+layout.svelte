<script lang="ts">
	import '../app.css';
	import { SvelteToast } from '@zerodevx/svelte-toast';
	let { children } = $props();
</script>

<SvelteToast />
{@render children()}

<style>
	:global {
		.confirmationDialog {
			background-color: aquamarine;
			max-width: 15rem;
			padding: 2rem;
		}

		.confirmationDialog::backdrop {
			backdrop-filter: blur(0.5rem);
		}

		.confirmationDialog .btnWrapper {
			margin: 2rem 0;
			display: flex;
			justify-content: space-around;
		}

		.confirmationDialog .confirm {
			background-color: greenyellow;
			padding: 0.5rem;
			border-radius: 10px;
		}

		.confirmationDialog .confirm:hover {
			background-color: aliceblue;
		}

		.confirmationDialog .cancel {
			background-color: royalblue;
			padding: 0.5rem;
			border-radius: 10px;
		}

		.confirmationDialog .cancel:hover {
			background-color: aliceblue;
		}
	}
</style>
