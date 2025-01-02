import type { Config } from 'tailwindcss';

export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {
			fontFamily: {
				"Agency-FB": ["Agency-FB", "Helvetica", "sans-serif"],
				"Bahnschrift": ["Bahnschrift", "Helvetica", "sans-serif"],
				"Arial": ["Arial", "Helvetica", "sans-serif"],
			},
			colors: {
				"vector-grey": "#e6e6e6",
				"vector-orange": "#ff4800"
			}
		},
	},

	plugins: []
} satisfies Config;
