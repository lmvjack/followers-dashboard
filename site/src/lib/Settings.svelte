<script lang="ts">
    import { get } from 'svelte/store';
    import { socialsArray } from './stores/socialsStore'
    import Input from './Input.svelte'

    let socials = get(socialsArray);
    

    const save = () => {
        for(let i = 0; i < socials.length; i++) {
            let usernameInput = (document.getElementById(`${socials[i]["name"]}-username`) as HTMLInputElement).value;
            if(usernameInput) {
                localStorage.setItem(`${socials[i]["name"]}-username`, usernameInput);
            }
        }
        location.reload();
    }

    const close = () => {
        let settings = document.getElementById("settings");
        settings.style.display = "none";
    }

    const deleteData = () => {
        localStorage.clear();
        location.reload();
    }
</script>

<h1>Settings</h1>


{#each socials as social}
    <Input {social} />
{/each}

<div class="settings-footer">
    <button on:click={deleteData}><i class="ph-bold ph-trash" style="color: red;"></i></button>
    <div class="right">
        <button class="cancel" on:click={close}>Close</button>
        <button class="save" on:click={save}>Save</button>
    </div>
    
</div>



<style>

    h1 {
        font-size: 2em;
        font-weight: 600;
        margin: 0;
    }

    .settings-footer {
        margin: auto 0 0 auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
    .right {
        display: flex;
        flex-direction: row;
        gap: 0.8em;
    }

    button {
        width: fit-content;
        border-radius: 8px;
        border: 0.6px solid transparent;
        padding: 0.6em 1.2em;
        font-size: 1em;
        font-weight: 500;
        font-family: inherit;
        cursor: pointer;
        transition: border-color 0.25s;
    }
    button:hover {
        border-color: white;
    }
    button:focus,
    button:focus-visible {
        outline: 4px auto -webkit-focus-ring-color;
    }
    .save {
        color: #181818;
        background-color: white;
    }
    .cancel {
        background-color: white;
        opacity: 0.6;
        color: #181818;
    }
</style>