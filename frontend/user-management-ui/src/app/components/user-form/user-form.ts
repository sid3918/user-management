import { Component, inject, OnInit, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { UserService } from '../../services/user.service';
import { UserPayload } from '../../models/user.model';

@Component({
  selector: 'app-user-form',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './user-form.html',
  styleUrl: './user-form.css',
})
export class UserForm implements OnInit {
  private fb = inject(FormBuilder);
  private userService = inject(UserService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  userId: number | null = null;
  saving = signal(false);
  errorMessage = signal('');
  today = new Date().toISOString().split('T')[0];

  form = this.fb.group({
    first_name: ['', [Validators.required, Validators.maxLength(100)]],
    last_name: ['', [Validators.required, Validators.maxLength(100)]],
    email: ['', [Validators.required, Validators.email, Validators.maxLength(255)]],
    phone: ['', [Validators.pattern(/^\+?\d{10,15}$/)]],
    gender: [''],
    date_of_birth: [''],
    department: ['', [Validators.maxLength(100)]],
    designation: ['', [Validators.maxLength(100)]],
    status: ['Active', [Validators.required]],
  });

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.userId = Number(id);
      this.userService.getUser(this.userId).subscribe({
        next: (user) => this.form.patchValue(user),
        error: (err) => {
          this.errorMessage.set(err.error?.detail || 'Could not load this user.');
        },
      });
    }
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.saving.set(true);
    this.errorMessage.set('');

    const payload = this.form.getRawValue() as UserPayload;
    const request =
      this.userId !== null
        ? this.userService.updateUser(this.userId, payload)
        : this.userService.createUser(payload);

    request.subscribe({
      next: () => {
        const message =
          this.userId !== null ? 'User updated successfully.' : 'User added successfully.';
        this.router.navigate(['/users'], { state: { message } });
      },
      error: (err) => {
        this.saving.set(false);
        if (err.status === 409 || err.status === 404) {
          this.errorMessage.set(err.error?.detail);
        } else if (err.status === 422) {
          this.errorMessage.set('Some values are not valid. Please check the form.');
        } else {
          this.errorMessage.set('Could not save the user. Please check that the backend is running.');
        }
      },
    });
  }
}