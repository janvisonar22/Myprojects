/** @odoo-module **/ 

import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";

// This variable will store the list of available voices.
let availableVoices = [];

// Function to load and cache voices asynchronously.
function loadVoices() {
	availableVoices = window.speechSynthesis.getVoices();
	if (availableVoices.length === 0) {
		window.speechSynthesis.addEventListener('voiceschanged', () => {
			availableVoices = window.speechSynthesis.getVoices();
			console.log("TTS Voices loaded successfully:", availableVoices.length);
		});
	} else {
		console.log("TTS Voices already loaded:", availableVoices.length);
	}
}

// Call loadVoices once when the module loads
loadVoices();

// Dedicated function to speak the text reliably
function startSpeech(text) {
	if (availableVoices.length === 0) {
		loadVoices(); 
		alert("Speech voices are still loading. Please try clicking 'Speak' again in a moment.");
		return;
	}

	let speech = new SpeechSynthesisUtterance(text);
	
	// --- KEY FIX: Do NOT assign a specific voice index. ---
	// Let the browser automatically select a voice based on 'lang' (en-US).
	// speech.voice = availableVoices[0]; // <--- REMOVED THIS BUGGY LINE
	
	speech.lang = "en-US"; // Set language for voice selection
	speech.rate = 1;
	speech.pitch = 1;
	
	// Stop any current speech and start the new one.
	window.speechSynthesis.cancel();
	window.speechSynthesis.speak(speech);

	console.log("TTS Speaking:", text);
}


// Patch FormController
patch(FormController.prototype, {
	
	async onButtonClick(params) {
		
		if (params.clickParams.name === "action_speak" && params.clickParams.type === "object") {
			
			const record = this.model.root;
			const text = record.data.name; 

			if (!text) {
				alert("Please enter some text to speak!");
				return;
			}

			// Call the dedicated speech function
			startSpeech(text);

			// Prevent Python dummy method from running
			return; 
		}

		return this._super.apply(this, arguments);
	},
});

































// /** @odoo-module **/

// import { FormController } from "@web/views/form/form_controller";
// import { patch } from "@web/core/utils/patch";

// // ----------------------------------------------------
// // Step 1: Create a reliable function to handle speech
// // ----------------------------------------------------

// // This variable will store the list of available voices.
// let availableVoices = [];

// // Function to load and cache voices asynchronously.
// function loadVoices() {
//     availableVoices = window.speechSynthesis.getVoices();
//     if (availableVoices.length === 0) {
//         // If voices are not yet loaded, set up a listener.
//         window.speechSynthesis.addEventListener('voiceschanged', () => {
//             availableVoices = window.speechSynthesis.getVoices();
//             console.log("TTS Voices loaded successfully:", availableVoices.length);
//         });
//     } else {
//         console.log("TTS Voices already loaded:", availableVoices.length);
//     }
// }

// // Call loadVoices once when the module loads
// loadVoices();

// // Dedicated function to speak the text reliably
// function startSpeech(text) {
//     if (availableVoices.length === 0) {
//         // Fallback: If voices still aren't ready, try loading them again and alert the user.
//         loadVoices(); 
//         alert("Speech voices are still loading. Please try clicking 'Speak' again in a moment.");
//         return;
//     }

//     let speech = new SpeechSynthesisUtterance(text);
	
//     // Choose the first available voice for guaranteed output.
//     speech.voice = availableVoices[0];
//     speech.lang = "en-US"; 
//     speech.rate = 1;
//     speech.pitch = 1;
	
//     // Stop any current speech and start the new one.
//     window.speechSynthesis.cancel();
//     window.speechSynthesis.speak(speech);

//     console.log("TTS Speaking:", text);
// }


// // ----------------------------------------------------
// // Step 2: Patch FormController to call the function
// // ----------------------------------------------------
// patch(FormController.prototype, {
	
//     async onButtonClick(params) {
		
//         if (params.clickParams.name === "action_speak" && params.clickParams.type === "object") {
			
//             const record = this.model.root;
//             // Ensure you are reading the data correctly
//             const text = record.data.name; 

//             if (!text) {
//                 alert("Please enter some text to speak!");
//                 return;
//             }

//             // Call the dedicated speech function
//             startSpeech(text);

//             // Prevent Python dummy method from running
//             return; 
//         }

//         // Call the original method for all other buttons
//         return this._super.apply(this, arguments);
//     },
// });