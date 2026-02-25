import { Header } from "./components/Header";

export const Layout = (props: any) => {
    return (
        <div style="display: flex; flex-direction: column; min-height: 100vh; color: white;">
            <Header />
            <main style="flex: 1; padding: 1rem;">
                {props.children}
            </main>
            <footer style="padding: 1rem; text-align: center;">
                &copy; 2026 Football League Simulator
            </footer>
        </div>
    );
};