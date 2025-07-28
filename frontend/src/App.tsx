import { CreatePostForm } from './features/feed/components/CreatePostForm';
import { PostList } from './features/feed/components/PostList';

function App() {
  return (
    <div className="container">
      <header>
        <h1>LDPL OJ Feed</h1>
      </header>
      <main>
        <CreatePostForm />
        <PostList />
      </main>
    </div>
  );
}

export default App;