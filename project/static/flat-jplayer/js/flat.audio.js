// jQuery(document).ready(function($) {
// 	$("#jquery_jplayer_audio_1").jPlayer({
// 		ready: function(event) {
// 			$(this).jPlayer("setMedia", {
// 				title: "Miaow - Hidden",
// 				mp3: "http://jplayer.org/audio/mp3/Miaow-02-Hidden.mp3",
// 				oga: "http://jplayer.org/audio/ogg/Miaow-02-Hidden.ogg"
// 			});
// 		},
// 		play: function() { // Avoid multiple jPlayers playing together.
// 			$(this).jPlayer("pauseOthers");
// 		},
// 		timeFormat: {
// 			padMin: false
// 		},
// 		swfPath: "js",
// 		supplied: "mp3,oga",
// 		cssSelectorAncestor: "#jp_container_audio_1",
// 		useStateClassSkin: true,
// 		autoBlur: false,
// 		smoothPlayBar: true,
// 		remainingDuration: true,
// 		keyEnabled: true,
// 		keyBindings: {
// 			// Disable some of the default key controls
// 			loop: null,
// 			muted: null,
// 			volumeUp: null,
// 			volumeDown: null
// 		},
// 		wmode: "window"
// 	});
// });
//
//
// jQuery(document).ready(function($) {
//
// 	function js_audioPlayer(audio, title, url) {
// 		$("#jplayer_audio_" + audio).jPlayer({
// 			ready: function () {
// 	      $(this).jPlayer("setMedia", {
// 					title: title,
// 					wav: url,
// 	      });
// 	    },
// 	    cssSelectorAncestor: "#jp_container_audio_" + audio,
// 		});
//
// 		play: function() { // Avoid multiple jPlayers playing together.
// 			$(this).jPlayer("pauseOthers");
// 		},
// 		timeFormat: {
// 			padMin: false
// 		},
// 		swfPath: "js",
// 		supplied: "mp3,wav",
// 		// cssSelectorAncestor: "#jp_container_audio_1",
// 		useStateClassSkin: true,
// 		autoBlur: false,
// 		smoothPlayBar: true,
// 		remainingDuration: true,
// 		keyEnabled: true,
// 		keyBindings: {
// 			// Disable some of the default key controls
// 			loop: null,
// 			muted: null,
// 			volumeUp: null,
// 			volumeDown: null
// 		},
// 		wmode: "window"
// 	});
//
//
//
// });
