<div id="followers-modal" class="hidden fixed z-50 inset-0 overflow-y-auto followers-model">
    <div class="flex items-center justify-center min-h-screen px-4">
        <div class="bg-white rounded-lg overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full">
            <div class="bg-gray-100 px-6 py-4">
                <h3 class="text-xl font-semibold text-gray-800 mb-4">followerss</h3>
                <!-- Set a specific height and make the followerss list scrollable -->
                <ul id="followerss-list-{{post.id}}" class="divide-y divide-gray-300 max-h-96 overflow-y-auto">
                    {% for followers in post.followerss.all %}
                    <li class="py-4">
                        <div class="flex items-start justify-between">
                            <div class="flex items-center">
                                <img class="h-10 w-10 rounded-full object-cover mr-4" src="{{ followers.posted_by.profile.photo.url }}" alt="{{ followers.posted_by.username }}">
                                <div>
                                    <p class="text-gray-800 font-semibold">{{ followers.posted_by.username }}</p>
                                    <p class="text-gray-600">{{ followers.body }}</p>
                                </div>
                            </div>
                            <p class="text-gray-400 text-sm">{{ followers.created }}</p> <!-- Display creation time -->
                        </div>
                    </li>
                    {% empty %}
                    <li class="py-4 text-gray-600">No followerss.</li>
                    {% endfor %}
                </ul>
            </div>
            <div class="bg-gray-200 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse followers-model-close">
                <button type="button" class="close-modal-btn inline-flex justify-center w-full px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                    Close
                </button>
            </div>
        </div>
    </div>
</div>

$(document).ready(function() {
    const followersButtons = document.querySelectorAll('.followers-btn');
    
    followersButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = button.dataset.postId;
            const followersModal = document.getElementById(`followers-modal-${ postId }`);
            followersModal.classList.remove('hidden');
        });
    });

    const closefollowersModalBtns = document.querySelectorAll('.close-modal-btn');
    closefollowersModalBtns.forEach(button => {
        button.addEventListener('click', function() {
            const modal = button.closest('.followers-model');
            modal.classList.add('hidden');
        });
    });

});