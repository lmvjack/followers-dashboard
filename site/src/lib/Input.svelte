<script lang="ts">
  import type { Social } from "./interfaces/social";
  
  export let social: Social;

  let capitalizedName: string = social.name.replace(social.name.charAt(0), social.name.charAt(0).toUpperCase());
</script>
  
  <h2>{capitalizedName}</h2>
  <input
    type="text"
    id="{social.name}-username"
    value={localStorage.getItem(`${social.name}-username`)}
    placeholder="Your {social.name} username here..."
  />
  
  <style>
    h2 {
      font-size: 1.4em;
      font-weight: 500;
      margin-bottom: 0.4em;
    }
  
    input {
      background-color: var(--settings);
      color: white;
      border: 1px solid #d9d9d9;
      border-radius: 5px;
      height: 50px;
      padding-left: 2%;
    }
  
    input:focus {
      outline: none;
      box-shadow: none;
    }
  </style>