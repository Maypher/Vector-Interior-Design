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
			background-color: var(--color-vector-grey);
			max-width: 30rem;
			padding: 2rem;
			margin: auto;
		}

		.confirmationDialog::backdrop {
			backdrop-filter: blur(0.5rem);
		}

		.confirmationDialog .btnWrapper {
			margin: 2rem 0;
			display: flex;
			justify-content: space-around;
		}

		.confirmationDialog button {
			transition: background-color 0.1s ease-in;
			cursor: pointer;
		}

		.confirmationDialog button:hover {
			filter: brightness(70%);
		}

		.confirmationDialog .confirm {
			background-color: red;
			padding: 0.5rem;
			border-radius: 10px;
		}

		.confirmationDialog .cancel {
			background-color: royalblue;
			padding: 0.5rem;
			border-radius: 10px;
		}
	}
</style>
