<script lang="ts">
    import type { Social } from "./interfaces/social";
  
    export let social: Social;

    async function fetchData(username: string, social: string) {
		const res = await fetch(`http://127.0.0.1:8000/${social}/${username}`);
		const json = await res.json();

		if (res.ok) {
			return json;
		} else {
			throw new Error(json);
		}
	}
</script>

<div class="bars-container">
    {#if localStorage.getItem(`${social.name}-username`)}

        {#await fetchData(localStorage.getItem(`${social.name}-username`), social.name)}
        <div class="bar">
            <i class="{social.icon}" style="color: {social.color}; font-size: 8em;"></i>
            <i class="ph ph-circle-notch loader" style="color: {social.color}"></i>
        </div>

        {:then data}
            <div class="bar">
                <i class="{social.icon}" style="color: {social.color}; font-size: 8em;"></i>
                <h2>{data.followers}</h2>
            </div>

        {:catch e}
        <p style="padding: 0 2em 0 2em; text-align: center;">❌ {social.name}: an error occurred! Check if the username is correct or try later.</p>
        {/await} 
    {/if}
</div>

<style>
    .bars-container {
        display: flex;
        flex-direction: column;
        gap: 1em;
    }

    .bar {
        display: flex;
        flex-direction: row;
        gap: 2em;
        align-items: center;
        justify-content: center;
    }

    h2 {
        font-size: 8em;
        margin: 0;
    }

    .loader {
        font-size: 6em;
        animation: spin 2s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @media (max-width: 1280px) {
        .bar {
            gap: 0.8em;
        }

        h2 {
            font-size: 3em;
        }

        .loader {
            font-size: 3em;
        }

        i {
            font-size: 3em !important;
        }
    }
</style>