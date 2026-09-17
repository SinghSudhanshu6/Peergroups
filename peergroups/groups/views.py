from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .models import Group, Membership, INTEREST_CHOICES
from .forms import GroupForm, CommentForm, PhotoForm, SignUpForm, ProfileForm


def home(request):
    """Browse / search groups, optionally filtered by interest tag."""
    groups = Group.objects.filter(meeting_time__gte=timezone.now())
    q = request.GET.get('q', '').strip()
    interest = request.GET.get('interest', '').strip()

    if q:
        groups = groups.filter(
            Q(name__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q)
        )
    if interest:
        groups = groups.filter(interest=interest)

    context = {
        'groups': groups,
        'interests': INTEREST_CHOICES,
        'q': q,
        'selected_interest': interest,
    }
    return render(request, 'groups/home.html', context)


def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    is_creator = request.user == group.creator

    membership = None
    if request.user.is_authenticated:
        membership = group.memberships.filter(user=request.user).first()
    is_member = bool(membership and membership.status == 'approved') or is_creator
    is_pending = bool(membership and membership.status == 'pending')

    comment_form = CommentForm()
    photo_form = PhotoForm()

    if request.method == 'POST' and request.user.is_authenticated:
        if 'post_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if not is_member:
                messages.error(request, 'Join the group before commenting.')
            elif comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.group = group
                comment.author = request.user
                comment.save()
                messages.success(request, 'Comment posted.')
                return redirect('group_detail', pk=pk)
        elif 'post_photo' in request.POST:
            photo_form = PhotoForm(request.POST, request.FILES)
            if not is_member:
                messages.error(request, 'Join the group before sharing photos.')
            elif photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.group = group
                photo.uploader = request.user
                photo.save()
                messages.success(request, 'Photo shared.')
                return redirect('group_detail', pk=pk)

    context = {
        'group': group,
        'is_member': is_member,
        'is_pending': is_pending,
        'is_creator': is_creator,
        'comments': group.comments.select_related('author') if is_member else [],
        'photos': group.photos.select_related('uploader') if is_member else [],
        'pending_requests': group.pending_requests if is_creator else [],
        'comment_form': comment_form,
        'photo_form': photo_form,
    }
    return render(request, 'groups/group_detail.html', context)


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            Membership.objects.create(group=group, user=request.user, status='approved')
            messages.success(request, f'"{group.name}" is live — share it with your classmates!')
            return redirect('group_detail', pk=group.pk)
    else:
        form = GroupForm()
    return render(request, 'groups/group_form.html', {'form': form, 'is_edit': False})


@login_required
def edit_group(request, pk):
    """Let the group leader change details — including date/time and location."""
    group = get_object_or_404(Group, pk=pk)
    if request.user != group.creator:
        messages.error(request, "Only the group leader can edit this group.")
        return redirect('group_detail', pk=pk)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group updated.')
            return redirect('group_detail', pk=pk)
    else:
        form = GroupForm(instance=group)
    return render(request, 'groups/group_form.html', {'form': form, 'is_edit': True, 'group': group})


@login_required
def join_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        status = 'pending' if group.is_private else 'approved'
        membership, created = Membership.objects.get_or_create(
            group=group, user=request.user, defaults={'status': status}
        )
        if created:
            if status == 'pending':
                messages.success(request, f'Request sent — the leader of {group.name} will review it.')
            else:
                messages.success(request, f'You joined {group.name}.')
    return redirect('group_detail', pk=pk)


@login_required
def leave_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        if group.creator == request.user:
            messages.error(request, "You created this group, so you can't leave it — you can delete it instead.")
        else:
            Membership.objects.filter(group=group, user=request.user).delete()
            messages.success(request, f'You left {group.name}.')
    return redirect('group_detail', pk=pk)


@login_required
def respond_to_request(request, pk, membership_id):
    """Group leader approves or rejects a pending join request (private groups)."""
    group = get_object_or_404(Group, pk=pk)

    if request.user != group.creator:
        messages.error(request, "Only the group leader can manage join requests.")
        return redirect('group_detail', pk=pk)

    membership = get_object_or_404(Membership, pk=membership_id, group=group)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            membership.status = 'approved'
            membership.save()
            messages.success(request, f'{membership.user.username} was added to the group.')
        elif action == 'reject':
            membership.delete()
            messages.success(request, f'Request from {membership.user.username} was declined.')
    return redirect('group_detail', pk=pk)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account is ready.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def edit_profile(request):
    """Let a user change their username and email."""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})
