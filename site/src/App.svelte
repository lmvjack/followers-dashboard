<script lang="ts">
  import { get } from 'svelte/store';
  import Settings from './lib/Settings.svelte'
  import Bar from './lib/Bar.svelte'
  import { socialsArray } from './lib/stores/socialsStore'

  let socials = get(socialsArray);

  const showSettings = () => {
    let settings = document.getElementById("settings");
    settings.style.display = "flex";
  }

  let unique = {} // every {} is unique, {} === {} evaluates to false

  export function restart() {
    unique = {}
  }
</script>

<main>
  <div class="bar-container">
    {#each socials as social}
      {#key unique}
        <Bar {social} />
      {/key}
    {/each}
  </div>

  <div class="main-buttons-container">
    <button class="show-settings-button" on:click={showSettings}>
      <i class="ph-bold ph-toggle-right" style="font-size: 1.6em;"></i>
    </button>
    <button class="reload-button" on:click={restart}>
      <i class="ph-bold ph-arrow-counter-clockwise" style="font-size: 1.4em; cursor: pointer;"></i>
    </button>
  </div>
  

  <div class="settings" id="settings">
    <Settings />
  </div>
</main>
