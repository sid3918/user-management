import { Component, inject, OnInit, signal } from '@angular/core';
import { UserService } from '../../services/user.service';
import { User } from '../../models/user.model';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-user-list',
  imports: [RouterLink],
  templateUrl: './user-list.html',
  styleUrl: './user-list.css',
})
export class UserList implements OnInit {
  private userService = inject(UserService);
  private router = inject(Router);
  
  users = signal<User[]>([]);
  loading = signal(true);
  errorMessage = signal('');
  successMessage = signal('');
  actionError = signal('');
  searchTerm = '';

  constructor() {
    const message = this.router.getCurrentNavigation()?.extras.state?.['message'];
    if (message) {
      this.successMessage.set(message);
    }
  }

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.loading.set(true);
    this.errorMessage.set('');

    this.userService.getUsers(this.searchTerm).subscribe({
      next: (users) => {
        this.users.set(users);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load users. Please check that the backend is running.');
        this.loading.set(false);
      },
    });
  }

  search(term: string): void {
  this.searchTerm = term.trim();
  this.loadUsers();
  }

  

  deleteUser(user: User): void {
    const confirmed = confirm(`Delete ${user.first_name} ${user.last_name}?`);
      if (!confirmed) {
        return;
      }

    this.successMessage.set('');
    this.actionError.set('');

    this.userService.deleteUser(user.user_id).subscribe({
        next: () => {
          this.successMessage.set('User deleted successfully.');
          this.loadUsers();
        },
        error: (err) => {
          this.actionError.set(err.error?.detail || 'Could not delete the user.');
        },
  });
}

}