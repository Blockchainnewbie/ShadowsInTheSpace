<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/auth'

// ...existing code...

const form = ref({
  email: '',
  password: ''
})
const error = ref('')

const router = useRouter()

const handleLogin = async () => {
  error.value = ''
  try {
    const response = await authService.login(form.value);
    console.log("Login Response:", response); // Log the entire response
    console.log("Status Code:", response.status); // Log the status code
    console.log("Response Headers:", response.headers); // Log the headers
    alert("Login erfolgreich!");
    router.push('/dashboard');
  } catch (err) {
    console.error("Fehler beim Login:", err);
    if (err.response) {
      console.log("Status Code:", err.response.status); // Log the status code
      console.log("Response Headers:", err.response.headers); // Log the headers
      if (err.response.data && err.response.data.message) {
        error.value = err.response.data.message;
      } else {
        error.value = 'Ein Fehler ist aufgetreten';
      }
    } else {
      error.value = 'Ein Fehler ist aufgetreten';
    }
  }
}

// ...existing code...
</script>
